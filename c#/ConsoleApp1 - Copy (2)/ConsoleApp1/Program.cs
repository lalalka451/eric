using System;
using System.IO;
using ServiceLib.Base;
using ServiceLib.Common;
using ServiceLib.Enums;
using ServiceLib.Handler;
using ServiceLib.Handler.CoreConfig;
using ServiceLib.Models;
using ServiceLib.ViewModels;
using Splat;
using System.Net.Http;



public class ConfigGenerator
{
    public static Action<SpeedTestResult> UpdateSpeedtestHandler { get; private set; }

    private static void HandleUpdate(bool notify, string msg)
    {
        // ... your logic to handle updates (e.gThe error "CS0119: 'UpdateHandler' is a type,., console output, logging) ...
    }

    public static void Main(string[] args)
    {
        //if (args.Length == 0)
        //{
        //    Console.WriteLine("Usage: ConfigGenerator <subscription_link_or_filepath>");
        //    return;
        //}

        //string input = args[0];

        // Read the input file

        // ... existing code ...



        string url = "https://imperialb.in/r/xjgxmgj0";
        string input = "";

        using (var client = new HttpClient())
        {
            input += client.GetStringAsync(url).Result;
        }

        // string input = File.ReadAllText("C:\\Users\\fueqq\\Downloads\\eric\\work\\python\\jobs (2)\\proxy_pool_lab\\input.txt");
        UpdateSpeedtestHandler = (result) =>
        {
            // Your logic for handling speed test results
            Console.WriteLine($"Speed Test Result: {result.IndexId} {result.Delay} {result.Speed}"); // Example


        };

        SQLiteHelper.Instance.Execute($"delete from ProfileExItem ");
        SQLiteHelper.Instance.Execute($"delete from ProfileItem ");


        // **KEY STEP: Initialize the Config**
        Config config = new Config();
        ConfigHandler.InitBuiltinRouting(config);
        ConfigHandler.InitBuiltinDNS(config);
        ConfigHandler.LoadConfig(ref config); // This may need adjustments for Linux
        LazyConfig.Instance.SetConfig(config);

        // Process the input data
        List<ProfileItem> lstAdd = ConfigHandler.AddBatchServers2(config, input, config.subIndexId, false);

        List<ServerTestItem> serverTestItems = new List<ServerTestItem>();
        foreach (var profileItem in lstAdd)
        {
            serverTestItems.Add(new ServerTestItem
            {
                indexId = profileItem.indexId,
                address = profileItem.address,
                port = profileItem.port,
                configType = profileItem.configType,
                allowTest = true
            });
        }

        // 2. Generate config.json for v2ray-core (for example)
        string fileName = Path.Combine(Utils.GetConfigPath(), "config_test.json");

        // Assuming you have a CoreType variable defined somewhere (e.g., ECoreType.V2Ray)
        ECoreType coreType = serverTestItems.Exists(t => t.configType == EConfigType.Hysteria2 || t.configType == EConfigType.Tuic || t.configType == EConfigType.Wireguard) ? ECoreType.sing_box : ECoreType.Xray;

        if (CoreConfigHandler.GenerateClientSpeedtestConfig(config, fileName, serverTestItems, coreType, out string msg) != 0)
        {
            //Console.WriteLine($"Error generating speed test config: {msg}");
        }

        Locator.CurrentMutable.Register(() => new CoreHandler(config, HandleUpdate), typeof(CoreHandler));

        var coreHandler = Locator.Current.GetService<CoreHandler>(); // Now it should be resolved correctly!
        if (coreHandler != null)
        {

            SpeedtestHandler _speedtestHandler = new SpeedtestHandler(config, coreHandler, lstAdd, ESpeedActionType.Mixedtest, UpdateSpeedtestHandler);
            //SpeedtestHandler _speedtestHandler = new SpeedtestHandler(config, coreHandler, lstAdd, ESpeedActionType.Realping, UpdateSpeedtestHandler);
        }

        // Wait for the user to press Enter before exiting
        Console.WriteLine("Press Enter to exit...");
        Console.ReadLine();

    }
}