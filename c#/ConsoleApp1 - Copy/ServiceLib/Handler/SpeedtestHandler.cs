using ServiceLib.ViewModels;
using Splat;
using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Text;
using static System.Net.Mime.MediaTypeNames;
using static System.Runtime.InteropServices.JavaScript.JSType;
// Import required namespaces
using System.Net.Http;
using System.Text;
using Newtonsoft.Json;

namespace ServiceLib.Handler
{
    public class SpeedtestHandler
    {
        private Config? _config;
        private CoreHandler _coreHandler;
        private List<ServerTestItem> _selecteds;
        private List<ProfileItem> _profileItems;
        List<ProfileItem> porfileItemFiltered;
        private ESpeedActionType _actionType;
        private Action<SpeedTestResult> _updateFunc;
        private bool _exitLoop = false;

        public SpeedtestHandler(Config config, CoreHandler coreHandler, List<ProfileItem> selecteds, ESpeedActionType actionType, Action<SpeedTestResult> update)
        {
            _config = config;
            _coreHandler = coreHandler;
            _actionType = actionType;
            _updateFunc = update;
            _profileItems = selecteds;

            _selecteds = new List<ServerTestItem>();
            foreach (var it in selecteds)
            {
                if (it.configType == EConfigType.Custom)
                {
                    continue;
                }
                if (it.port <= 0)
                {
                    continue;
                }
                _selecteds.Add(new ServerTestItem()
                {
                    indexId = it.indexId,
                    address = it.address,
                    port = it.port,
                    configType = it.configType
                });
            }
            //clear test result
            foreach (var it in _selecteds)
            {
                switch (actionType)
                {
                    case ESpeedActionType.Tcping:
                    case ESpeedActionType.Realping:
                        UpdateFunc(it.indexId, ResUI.Speedtesting, "");
                        ProfileExHandler.Instance.SetTestDelay(it.indexId, "0");
                        break;

                    case ESpeedActionType.Speedtest:
                        UpdateFunc(it.indexId, "", ResUI.SpeedtestingWait);
                        ProfileExHandler.Instance.SetTestSpeed(it.indexId, "0");
                        break;

                    case ESpeedActionType.Mixedtest:
                        UpdateFunc(it.indexId, ResUI.Speedtesting, ResUI.SpeedtestingWait);
                        ProfileExHandler.Instance.SetTestDelay(it.indexId, "0");
                        ProfileExHandler.Instance.SetTestSpeed(it.indexId, "0");
                        break;
                    case ESpeedActionType.CustomMixedtest:
                        UpdateFunc(it.indexId, ResUI.Speedtesting, ResUI.SpeedtestingWait);
                        ProfileExHandler.Instance.SetTestDelay(it.indexId, "0");
                        ProfileExHandler.Instance.SetTestSpeed(it.indexId, "0");
                        break;
                }
            }

            switch (actionType)
            {
                case ESpeedActionType.Tcping:
                    Task.Run(RunTcping);
                    break;

                case ESpeedActionType.Realping:
                    Task.Run(RunRealPing);
                    break;

                case ESpeedActionType.Speedtest:
                    Task.Run(RunSpeedTestAsync);
                    break;

                case ESpeedActionType.Mixedtest:
                    Task.Run(RunMixedtestAsync);
                    break;

            }
        }

        public void ExitLoop()
        {
            _exitLoop = true;
            UpdateFunc("", ResUI.SpeedtestingStop);
        }

        private Task RunTcping()
        {
            try
            {
                List<Task> tasks = [];
                foreach (var it in _selecteds)
                {
                    if (it.configType == EConfigType.Custom)
                    {
                        continue;
                    }
                    tasks.Add(Task.Run(() =>
                    {
                        try
                        {
                            int time = GetTcpingTime(it.address, it.port);
                            var output = FormatOut(time, Global.DelayUnit);

                            ProfileExHandler.Instance.SetTestDelay(it.indexId, output);
                            UpdateFunc(it.indexId, output);
                        }
                        catch (Exception ex)
                        {
                            Logging.SaveLog(ex.Message, ex);
                        }
                    }));
                }
                Task.WaitAll([.. tasks]);
            }
            catch (Exception ex)
            {
                Logging.SaveLog(ex.Message, ex);
            }
            finally
            {
                ProfileExHandler.Instance.SaveTo();
            }

            return Task.CompletedTask;
        }

        private Task RunRealPing()
        {
            int pid = -1;
            try
            {
                string msg = string.Empty;

                pid = _coreHandler.LoadCoreConfigSpeedtest(_selecteds);
                if (pid < 0)
                {
                    UpdateFunc("", ResUI.FailedToRunCore);
                    return Task.CompletedTask;
                }

                DownloadHandler downloadHandle = new DownloadHandler();

                List<Task> tasks = new();
                foreach (var it in _selecteds)
                {
                    if (!it.allowTest)
                    {
                        continue;
                    }
                    if (it.configType == EConfigType.Custom)
                    {
                        continue;
                    }
                    tasks.Add(Task.Run(async () =>
                    {
                        try
                        {
                            WebProxy webProxy = new(Global.Loopback, it.port);
                            string output = await GetRealPingTime(downloadHandle, webProxy);

                            ProfileExHandler.Instance.SetTestDelay(it.indexId, output);
                            UpdateFunc(it.indexId, output);
                            int.TryParse(output, out int delay);
                            it.delay = delay;
                        }
                        catch (Exception ex)
                        {
                            Logging.SaveLog(ex.Message, ex);
                        }
                    }));
                }
                Task.WaitAll(tasks.ToArray());
            }
            catch (Exception ex)
            {
                Logging.SaveLog(ex.Message, ex);
            }
            finally
            {
                if (pid > 0)
                {
                    _coreHandler.CoreStopPid(pid);
                }
                var lstExists = SQLiteHelper.Instance.Table<ProfileExItem>();
                List<ProfileExItem> lstInserts = [];
                List<ProfileExItem> lstUpdates = [];

                porfileItemFiltered = ProfileExHandler.Instance.SaveTo2(_profileItems);

                //List<ProfileItem> porfileItemFiltered = ProfileExHandler.Instance.Filter(_profileItems);

            }

            return Task.CompletedTask;
        }

        private async Task RunSpeedTestAsync()
        {
            int pid = -1;
            //if (_actionType == ESpeedActionType.Mixedtest)
            //{
            //    _selecteds = _selecteds.OrderBy(t => t.delay).ToList();
            //}

            pid = _coreHandler.LoadCoreConfigSpeedtest(_selecteds);
            if (pid < 0)
            {
                UpdateFunc("", ResUI.FailedToRunCore);
                return;
            }

            string url = _config.speedTestItem.speedTestUrl;
            var timeout = _config.speedTestItem.speedTestTimeout;

            DownloadHandler downloadHandle = new();

            foreach (var it in _selecteds)
            {
                if (_exitLoop)
                {
                    UpdateFunc(it.indexId, "", ResUI.SpeedtestingSkip);
                    continue;
                }
                if (!it.allowTest)
                {
                    continue;
                }
                if (it.configType == EConfigType.Custom)
                {
                    continue;
                }
                //if (it.delay < 0)
                //{
                //    UpdateFunc(it.indexId, "", ResUI.SpeedtestingSkip);
                //    continue;
                //}
                ProfileExHandler.Instance.SetTestSpeed(it.indexId, "-1");
                UpdateFunc(it.indexId, "", ResUI.Speedtesting);

                var item = LazyConfig.Instance.GetProfileItem(it.indexId);
                if (item is null) continue;

                WebProxy webProxy = new(Global.Loopback, it.port);

                await downloadHandle.DownloadDataAsync(url, webProxy, timeout, (bool success, string msg) =>
                {
                    decimal.TryParse(msg, out decimal dec);
                    if (dec > 0)
                    {
                        ProfileExHandler.Instance.SetTestSpeed(it.indexId, msg);
                    }
                    UpdateFunc(it.indexId, "", msg);
                });
            }

            if (pid > 0)
            {
                _coreHandler.CoreStopPid(pid);
            }
            UpdateFunc("", ResUI.SpeedtestingCompleted);
            ProfileExHandler.Instance.SaveTo();
        }

        private async Task RunSpeedTestMulti()
        {
            int pid = -1;
            pid = _coreHandler.LoadCoreConfigSpeedtest(_selecteds);
            if (pid < 0)
            {
                UpdateFunc("", ResUI.FailedToRunCore);
                return;
            }

            string url = _config.speedTestItem.speedTestUrl;
            var timeout = _config.speedTestItem.speedTestTimeout;

            DownloadHandler downloadHandle = new();

            foreach (var it in _selecteds)
            {
                if (_exitLoop)
                {
                    UpdateFunc(it.indexId, "", ResUI.SpeedtestingSkip);
                    continue;
                }

                if (!it.allowTest)
                {
                    continue;
                }
                if (it.configType == EConfigType.Custom)
                {
                    continue;
                }
                if (it.delay < 0)
                {
                    UpdateFunc(it.indexId, "", ResUI.SpeedtestingSkip);
                    continue;
                }
                ProfileExHandler.Instance.SetTestSpeed(it.indexId, "-1");
                UpdateFunc(it.indexId, "", ResUI.Speedtesting);

                var item = LazyConfig.Instance.GetProfileItem(it.indexId);
                if (item is null) continue;

                WebProxy webProxy = new(Global.Loopback, it.port);
                _ = downloadHandle.DownloadDataAsync(url, webProxy, timeout, (bool success, string msg) =>
                {
                    decimal.TryParse(msg, out decimal dec);
                    if (dec > 0)
                    {
                        ProfileExHandler.Instance.SetTestSpeed(it.indexId, msg);
                    }
                    UpdateFunc(it.indexId, "", msg);
                });
                await Task.Delay(2000);
            }

            await Task.Delay((timeout + 2) * 1000);

            if (pid > 0)
            {
                _coreHandler.CoreStopPid(pid);
            }
            UpdateFunc("", ResUI.SpeedtestingCompleted);
            ProfileExHandler.Instance.SaveTo();



            List<ProfileItem> _selecteds2 = new List<ProfileItem>();

            //get all proxy speed is -1
            foreach (var it in _selecteds)
            {
                if (it.configType == EConfigType.Custom)
                {
                    continue;
                }
                decimal speed = ProfileExHandler.Instance.GetSpeed(it.indexId);
                if (it.delay == -1 || speed == -1)
                {

                    var item = LazyConfig.Instance.GetProfileItem(it.indexId);
                    _selecteds2.Add(item);
                }

            }
            ConfigHandler.RemoveServer(_config, _selecteds2.ToList());

        }




        public async Task UpdateDocumentOnImperialAsync(string documentId, string obj)
        {
            var imperialUrl = "";

            var url = "https://api.impb.in/v1/document";
            var client = new HttpClient();
            client.DefaultRequestHeaders.Add("Authorization", "imperial_c185M2YxZGVjNjE0NThhN2I4YTIwNzRhNTc2Mjc3OTFhOV8zNjAwOTg5OTYzNDM3NzkzNTM");
    

            var data = new
            {
                id = documentId, // Include the document ID
                content = obj
            };


            var json = JsonConvert.SerializeObject(data);
            var stringContent = new StringContent(json, Encoding.UTF8, "application/json");

            try
            {
                var response = await client.PatchAsync(url, stringContent);

                // Check the status code explicitly
                if (!response.IsSuccessStatusCode)
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    UpdateFunc("", $"Failed to update Imperial document: Status code {response.StatusCode} - {errorContent}");
                    return;
                }

                var result = await response.Content.ReadAsStringAsync();
                var jsonResult = JsonConvert.DeserializeObject<dynamic>(result);
                imperialUrl = $"https://impb.in/{jsonResult.data.id}";

                UpdateFunc("", $"Document updated successfully on Imperial. URL: {imperialUrl}");
            }
            catch (HttpRequestException e)
            {
                UpdateFunc("", $"Failed to update Imperial document: {e.Message}");
            }
    }

        private async Task RunMixedtestAsync()
        {
            // https://imperialb.in/zfx0pqjn
            // json core config file
            var documentId = "zfx0pqjn";
            var obj = File.ReadAllText("guiConfigs\\config_test.json");
            await UpdateDocumentOnImperialAsync(documentId, obj);
            await RunRealPing();



            await Task.Delay(1000);

            //await RunSpeedTestMulti();

            UpdateFunc("", "iamhere");

 
            var contentToUpload = string.Join("\n", porfileItemFiltered.Select(item => item.originalProxy));
            if (contentToUpload != "")
            {
                // https://imperialb.in/0pqvgb0s
                // valid non encode proxy file
                documentId = "0pqvgb0s";
                await UpdateDocumentOnImperialAsync(documentId, contentToUpload);

                // https://imperialb.in/fkepmqwb
                // valid encoded proxy file
                documentId = "fkepmqwb";
                string encodedData = Convert.ToBase64String(Encoding.UTF8.GetBytes(contentToUpload));
                await UpdateDocumentOnImperialAsync(documentId, encodedData);

                // https://imperialb.in/ywkbzmxe
                // valid port file

                var contentToUpload1 = string.Join("\n", porfileItemFiltered.Select(item => item.port));
                documentId = "ywkbzmxe";
                if (contentToUpload != "")
                {
                    await UpdateDocumentOnImperialAsync(documentId, contentToUpload1);
                }
            }

       




            //Locator.Current.GetService<ProfilesViewModel>()?.RemoveDuplicateServer();

            // Now, update the UI after both asynchronous tasks have completed
            //await UpdateFunc2("", ResUI.SpeedtestingCompleted);
        }

        private async Task UpdateFunc2(string indexId, string delay, string speed = "")
        {
            await Task.Run(() =>
            {

                _updateFunc(new() { IndexId = indexId, Delay = delay, Speed = speed });
            });
        }


        private async Task<string> GetRealPingTime(DownloadHandler downloadHandle, IWebProxy webProxy)
        {
            int responseTime = await downloadHandle.GetRealPingTime(_config.speedTestItem.speedPingTestUrl, webProxy, 10);
            //string output = Utile.IsNullOrEmpty(status) ? FormatOut(responseTime, "ms") : status;
            return FormatOut(responseTime, Global.DelayUnit);
        }

        private int GetTcpingTime(string url, int port)
        {
            int responseTime = -1;

            try
            {
                if (!IPAddress.TryParse(url, out IPAddress? ipAddress))
                {
                    IPHostEntry ipHostInfo = System.Net.Dns.GetHostEntry(url);
                    ipAddress = ipHostInfo.AddressList[0];
                }

                var timer = Stopwatch.StartNew();

                IPEndPoint endPoint = new(ipAddress, port);
                using Socket clientSocket = new(endPoint.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

                var result = clientSocket.BeginConnect(endPoint, null, null);
                if (!result.AsyncWaitHandle.WaitOne(TimeSpan.FromSeconds(5)))
                    throw new TimeoutException("connect timeout (5s): " + url);
                clientSocket.EndConnect(result);

                timer.Stop();
                responseTime = (int)timer.Elapsed.TotalMilliseconds;
            }
            catch (Exception ex)
            {
                Logging.SaveLog(ex.Message, ex);
            }
            return responseTime;
        }

        private string FormatOut(object time, string unit)
        {
            //if (time.ToString().Equals("-1"))
            //{
            //    return "Timeout";
            //}
            return $"{time}";
        }

        private void UpdateFunc(string indexId, string delay, string speed = "")
        {
            _updateFunc(new() { IndexId = indexId, Delay = delay, Speed = speed });
        }
    }
}