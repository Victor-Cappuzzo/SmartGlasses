package com.example.smartglassesapp

import android.Manifest
import android.app.NotificationManager
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.*
import android.content.pm.PackageManager
import androidx.appcompat.app.AppCompatActivity
import android.service.notification.NotificationListenerService
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.lifecycle.ViewModelProvider
import com.example.smartglassesapp.databinding.ActivityMainBinding
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import java.io.IOException
import java.io.InputStream
import java.io.OutputStream
import java.util.*
import androidx.lifecycle.Observer
import android.content.ComponentName
import android.os.*
import android.provider.Settings

class MainActivity : AppCompatActivity() {

    // Variable declarations
    private lateinit var binding: ActivityMainBinding
    private var messageEditText: EditText? = null
    private var timeTextView: TextView? = null
    private var sendButton: Button? = null
    private var batteryTextView: TextView? = null
    private var chargingTextView: TextView? = null
    private lateinit var model: AppViewModel
    private lateinit var dataTransmissionService: DataTransmissionService
    private var isDataTransmissionBound: Boolean = false

    private val notificationReceiver = object: BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == "com.example.smartglassesapp.APP_STARTED") {
                //sendExistingNotifications(applicationContext)
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Start the NotificationListenerService
        if (!isNotificationServiceEnabled()) {
            startActivity(Intent("android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS"))
        }

        // Initialize view model
        model = ViewModelProvider(this).get(AppViewModel::class.java)

        // Variable initialization
        messageEditText = binding.messageEditText
        timeTextView = binding.timeTextView
        sendButton = binding.sendButton
        batteryTextView = binding.batteryTextView
        chargingTextView = binding.chargingTextView

        // Listen for if the send button is pressed
        sendButton!!.setOnClickListener {
            val message = messageEditText!!.text.toString()
            if (isDataTransmissionBound) {
                //dataTransmissionService.addMessageToQueue("M:::$message")
                model.sendCustomMessage(applicationContext, message)
            }
        }


        // Set observer for the current time and date value
        val dateTimeObserver = Observer<String> {newDateTime ->
                timeTextView!!.text = newDateTime
        }
        model.getDateAndTime().observe(this, dateTimeObserver)

        // Start updating the date and time
        model.updateDateAndTime(applicationContext)


        // Set observer for the current battery percentage
        val batteryPercentObserver = Observer<Int> {newPercent ->
            batteryTextView!!.text = "$newPercent%"
        }
        model.getBatteryPercent().observe(this, batteryPercentObserver)

        // Start updating the battery percentage
        model.updateBatteryPercent(applicationContext)


        // Set observer for the current battery charging status
        val batteryChargingObserver = Observer<Boolean> {isCharging ->

            // If the phone is charging
            if (isCharging) {
                chargingTextView!!.text = "ON"
            }

            // If the phone is not charging
            else {
                chargingTextView!!.text = "OFF"
            }

        }
        model.getBatteryCharging().observe(this, batteryChargingObserver)

        // Start updating the battery charging status
        model.updateBatteryCharging(applicationContext)

        // Register the BroadcastReceiver
        val filter = IntentFilter("com.example.smartglassesapp.APP_STARTED")
        registerReceiver(notificationReceiver, filter)

        // Send existing notifications when the app starts
        val appStartedIntent = Intent("com.example.smartglassesapp.APP_STARTED")
        sendBroadcast(appStartedIntent)

        // Send existing notifications
        //sendExistingNotifications(applicationContext)

    }

    override fun onStart() {
        super.onStart()
        val intent = Intent(this, DataTransmissionService::class.java)
        bindService(intent, dataTransmissionServiceConnection, Context.BIND_AUTO_CREATE)
    }

    override fun onStop() {
        super.onStop()
        if (isDataTransmissionBound) {
            unbindService(dataTransmissionServiceConnection)
            isDataTransmissionBound = false
        }
    }

    override fun onDestroy() {
        super.onDestroy()

        // Unregister the BroadcastReceiver when the activity is destroyed
        unregisterReceiver(notificationReceiver)
    }

    private val dataTransmissionServiceConnection = object : ServiceConnection {
        override fun onServiceConnected(name: ComponentName?, service: IBinder?) {
            val binder = service as DataTransmissionService.DataTransmissionBinder
            dataTransmissionService = binder.getService()
            isDataTransmissionBound = true
        }

        override fun onServiceDisconnected(name: ComponentName?) {
            isDataTransmissionBound = false
        }
    }

    /*
    private fun sendExistingNotifications(context: Context) {

        // Get the current notification manager
        val notificationManager =
            context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // Get the active notifications
        val activeNotifications = notificationManager.activeNotifications

        // Send each notification app and count
        for (notification in activeNotifications) {
            val appName = notification.packageName
            val notificationCount = activeNotifications.filter { it.packageName == appName }.size

            // Send app name and count via Bluetooth DataTransmissionService
            model.sendMessageToService(context, "N:::$appName,$notificationCount")
        }
    }

     */

    private fun isNotificationServiceEnabled(): Boolean {
        val componentName = ComponentName(this, NotificationListener::class.java)
        val flat: String = Settings.Secure.getString(contentResolver, "enabled_notification_listeners")
        return flat != null && flat.contains(componentName.flattenToString())
    }

}