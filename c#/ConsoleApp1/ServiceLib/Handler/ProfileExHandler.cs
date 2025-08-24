using DynamicData;
using ServiceLib.Models;
using System.Collections.Concurrent;

//using System.Reactive.Linq;

namespace ServiceLib.Handler
{
    public class ProfileExHandler
    {
        private static readonly Lazy<ProfileExHandler> _instance = new(() => new());
        private ConcurrentBag<ProfileExItem> _lstProfileEx = [];
        private Queue<string> _queIndexIds = new();
        public ConcurrentBag<ProfileExItem> ProfileExs => _lstProfileEx;
        public static ProfileExHandler Instance => _instance.Value;

        public ProfileExHandler()
        {
            Init();

            Task.Run(async () =>
            {
                while (true)
                {
                    SaveQueueIndexIds();
                    await Task.Delay(1000 * 600);
                }
            });
        }

        private void Init()
        {
            SQLiteHelper.Instance.Execute($"delete from ProfileExItem where indexId not in ( select indexId from ProfileItem )");

            _lstProfileEx = new(SQLiteHelper.Instance.Table<ProfileExItem>());
        }

        private void IndexIdEnqueue(string indexId)
        {
            if (!Utils.IsNullOrEmpty(indexId) && !_queIndexIds.Contains(indexId))
            {
                _queIndexIds.Enqueue(indexId);
            }
        }

        private void SaveQueueIndexIds()
        {
            var cnt = _queIndexIds.Count;
            if (cnt > 0)
            {
                var lstExists = SQLiteHelper.Instance.Table<ProfileExItem>();
                List<ProfileExItem> lstInserts = [];
                List<ProfileExItem> lstUpdates = [];

                for (int i = 0; i < cnt; i++)
                {
                    var id = _queIndexIds.Dequeue();
                    var item = lstExists.FirstOrDefault(t => t.indexId == id);
                    var itemNew = _lstProfileEx?.FirstOrDefault(t => t.indexId == id);
                    if (itemNew is null)
                    {
                        continue;
                    }

                    if (item is not null)
                    {
                        lstUpdates.Add(itemNew);
                    }
                    else
                    {
                        lstInserts.Add(itemNew);
                    }
                }
                try
                {
                    if (lstInserts.Count() > 0)
                        SQLiteHelper.Instance.InsertAll(lstInserts);

                    if (lstUpdates.Count() > 0)
                        SQLiteHelper.Instance.UpdateAll(lstUpdates);
                }
                catch (Exception ex)
                {
                    Logging.SaveLog("ProfileExHandler", ex);
                }
            }
        }

        private List<ProfileItem> SaveQueueIndexIds2(List<ProfileItem> profileItems)
        {
            var cnt = _queIndexIds.Count;
            List<ProfileItem> profileitemsFilter = [];
            if (cnt > 0)
            {
                var lstExists = SQLiteHelper.Instance.Table<ProfileExItem>();
                List<ProfileExItem> lstInserts = [];
                List<ProfileExItem> lstUpdates = [];

                for (int i = 0; i < cnt; i++)
                {
                    var id = _queIndexIds.Dequeue();

                    var testedItem = profileItems?.FirstOrDefault(t => t.indexId == id);
                    //ProfileExItem item1 = lstExists.FirstOrDefault(t => t.indexId == id);
                    var item = lstExists.FirstOrDefault(t => t.indexId == id);
                    var itemNew = _lstProfileEx?.FirstOrDefault(t => t.indexId == id);
                    if (itemNew is null)
                    {
                        continue;
                    }

                    if (item is not null)
                    {
                        lstUpdates.Add(itemNew);
                        if (item.delay != -1) { 
                            profileitemsFilter.Add(testedItem);
                        }
                    }
                    else
                    {
                        lstInserts.Add(itemNew);
                        if (itemNew.delay != -1)
                        {
                            profileitemsFilter.Add(testedItem);
                        }
                    }
                }
                try
                {
                    if (lstInserts.Count() > 0)
                        SQLiteHelper.Instance.InsertAll(lstInserts);

                    if (lstUpdates.Count() > 0)
                        SQLiteHelper.Instance.UpdateAll(lstUpdates);
                }
                catch (Exception ex)
                {
                    Logging.SaveLog("ProfileExHandler", ex);
                }
            }
            return profileitemsFilter;
        }

        private List<ProfileItem> FilterQueueIndexIds(List<ProfileItem> profileItems)
        {
            var cnt = _queIndexIds.Count;
            List<ProfileItem> profileitemsFilter = [];
            var lstExists = SQLiteHelper.Instance.Table<ProfileExItem>();

            for (int i = 0; i < cnt; i++)
            {
                var id = _queIndexIds.Dequeue();
                var testedItem = profileItems?.FirstOrDefault(t => t.indexId == id);
                ProfileExItem item = lstExists.FirstOrDefault(t => t.indexId == id);
                if (item is null) {
                    continue;
                }
                if (testedItem is null || item.delay != -1)
                    {
                    continue;
                }

                profileitemsFilter.Add(testedItem);
            }
            return profileitemsFilter;
        }

        private void AddProfileEx(string indexId, ref ProfileExItem? profileEx)
        {
            profileEx = new()
            {
                indexId = indexId,
                delay = 0,
                speed = 0,
                sort = 0
            };
            _lstProfileEx.Add(profileEx);
            IndexIdEnqueue(indexId);
        }

        public void ClearAll()
        {
            SQLiteHelper.Instance.Execute($"delete from ProfileExItem ");
            _lstProfileEx = new();
        }

        public List<ProfileItem> Filter(List<ProfileItem> profileItems)
        {
   
            List<ProfileItem> profileItemsFiltered = FilterQueueIndexIds(profileItems);
            return profileItemsFiltered;
        }

        public List<ProfileItem> SaveTo2(List<ProfileItem> profileItems)
        {
    
            List<ProfileItem> profileItemsFiltered = SaveQueueIndexIds2(profileItems);
            return profileItemsFiltered;

        }
        public void SaveTo()
        {
            try
            {
                SaveQueueIndexIds();
            }
            catch (Exception ex)
            {
                Logging.SaveLog(ex.Message, ex);
            }
        }

        public void SetTestDelay(string indexId, string delayVal)
        {
            var profileEx = _lstProfileEx.FirstOrDefault(t => t.indexId == indexId);
            if (profileEx == null)
            {
                AddProfileEx(indexId, ref profileEx);
            }

            int.TryParse(delayVal, out int delay);
            profileEx.delay = delay;
            IndexIdEnqueue(indexId);
        }

        public void SetTestSpeed(string indexId, string speedVal)
        {
            var profileEx = _lstProfileEx.FirstOrDefault(t => t.indexId == indexId);
            if (profileEx == null)
            {
                AddProfileEx(indexId, ref profileEx);
            }

            decimal.TryParse(speedVal, out decimal speed);
            profileEx.speed = speed;
            IndexIdEnqueue(indexId);
        }

        public void SetSort(string indexId, int sort)
        {
            var profileEx = _lstProfileEx.FirstOrDefault(t => t.indexId == indexId);
            if (profileEx == null)
            {
                AddProfileEx(indexId, ref profileEx);
            }
            profileEx.sort = sort;
            IndexIdEnqueue(indexId);
        }

        public decimal GetSpeed(string indexId)
        {
            var profileEx = _lstProfileEx.FirstOrDefault(t => t.indexId == indexId);
            if (profileEx == null)
            {
                return 0;
            }
            return profileEx.speed;
        }

        public int GetSort(string indexId)
        {
            var profileEx = _lstProfileEx.FirstOrDefault(t => t.indexId == indexId);
            if (profileEx == null)
            {
                return 0;
            }
            return profileEx.sort;
        }

        public int GetMaxSort()
        {
            if (_lstProfileEx.Count <= 0)
            {
                return 0;
            }
            return _lstProfileEx.Max(t => t == null ? 0 : t.sort);
        }
    }
}