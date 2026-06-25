cordova.define('cordova/plugin_list', function(require, exports, module) {
module.exports = [
  {
    "id": "com.capacitorjs.plugins.keyboard.KeyboardPlugin",
    "file": "plugins/@capacitor/keyboard/0.js",
    "pluginId": "capacitor-keyboard"
  },
  {
    "id": "com.capacitorjs.plugins.localnotifications.LocalNotificationsPlugin",
    "file": "plugins/@capacitor/local-notifications/0.js",
    "pluginId": "capacitor-local-notifications"
  },
  {
    "id": "com.capacitorjs.plugins.splashscreen.SplashScreenPlugin",
    "file": "plugins/@capacitor/splash-screen/0.js",
    "pluginId": "capacitor-splash-screen"
  },
  {
    "id": "com.capacitorjs.plugins.statusbar.StatusBarPlugin",
    "file": "plugins/@capacitor/status-bar/0.js",
    "pluginId": "capacitor-status-bar"
  }
];
module.exports.metadata = {
  "com.capacitorjs.plugins.keyboard": "6.0.4",
  "com.capacitorjs.plugins.local-notifications": "6.1.3",
  "com.capacitorjs.plugins.splash-screen": "6.0.4",
  "com.capacitorjs.plugins.status-bar": "6.0.3"
};
});
