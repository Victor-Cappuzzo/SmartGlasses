package com.example.smartglassesapp

import android.app.NotificationManager
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlin.coroutines.CoroutineContext
import kotlinx.coroutines.*
import java.text.SimpleDateFormat
import java.util.*

class AppViewModel: ViewModel() {

    // Time and Date variables
    private val sdf = SimpleDateFormat("h:mm a")
    private val currentDateTimeLiveData = MutableLiveData<String>()
    private var currentDateTimeLocal = sdf.format(Date())
    private val timeDateDelay: Long = 100
    private lateinit var timeDateJob: Job
    private lateinit var timeDateScope: CoroutineScope

    // Battery Percentage variables
    private val currentBatteryPercentLiveData = MutableLiveData<Int>()
    private var currentBatteryPercentLocal: Int = 0
    private val batteryPercentDelay: Long = 10000
    private lateinit var batteryPercentJob: Job
    private lateinit var batteryPercentScope: CoroutineScope

    // Battery Charging Status variables
    private val currentBatteryChargingLiveData = MutableLiveData<Boolean>()
    private var currentBatteryChargingLocal: Boolean = false
    private val batteryChargingDelay: Long = 1000
    private lateinit var batteryChargingJob: Job
    private lateinit var batteryChargingScope: CoroutineScope

    // Notification variables
    private val notificationDelay: Long = 1000
    private lateinit var notificationJob: Job
    private lateinit var notificationScope: CoroutineScope

    init {
        timeDateJob = Job()
        timeDateScope = CoroutineScope(Dispatchers.IO + timeDateJob)
        currentDateTimeLiveData.postValue(currentDateTimeLocal)

        batteryPercentJob = Job()
        batteryPercentScope = CoroutineScope(Dispatchers.IO + batteryPercentJob)
        currentBatteryPercentLiveData.postValue(currentBatteryPercentLocal)

        batteryChargingJob = Job()
        batteryChargingScope = CoroutineScope(Dispatchers.IO + batteryChargingJob)
        currentBatteryChargingLiveData.postValue(currentBatteryChargingLocal)

        notificationJob = Job()
        notificationScope = CoroutineScope(Dispatchers.IO + notificationJob)
    }


    // Send a message to the DataTransmissionService
    fun sendMessageToService(context: Context, message: String) {
        val serviceIntent = Intent(context, DataTransmissionService::class.java)
        serviceIntent.putExtra("message", message)
        context.startService(serviceIntent)
    }

    fun sendCustomMessage(context: Context, str: String) {
        sendMessageToService(context, "M:::$str")
    }


    // Update the current date and time
    fun updateDateAndTime(context: Context) {

        timeDateJob.cancel()

        timeDateJob = CoroutineScope(Dispatchers.IO).launch {

            while (true) {
                currentDateTimeLocal = sdf.format(Date())

                if (currentDateTimeLiveData.value != currentDateTimeLocal) {

                    // Post live data to update the UI
                    currentDateTimeLiveData.postValue(currentDateTimeLocal)

                    // Start the DataTransmissionService
                    sendMessageToService(context, "T:::$currentDateTimeLocal")
                }

                delay(timeDateDelay)
            }
        }
    }

    // Returns the current date and time
    fun getDateAndTime(): LiveData<String> {
        return currentDateTimeLiveData
    }


    // Get the current battery percentage
    fun updateBatteryPercent(context: Context) {

        batteryPercentJob.cancel()

        batteryPercentJob = CoroutineScope(Dispatchers.IO).launch {

            while (true) {

                // Get the current battery status intent
                val batteryStatus: Intent? = IntentFilter(Intent.ACTION_BATTERY_CHANGED).let { ifilter ->
                    context.registerReceiver(null, ifilter)
                }

                currentBatteryPercentLocal = batteryStatus?.let { intent ->
                    val level: Int = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
                    val scale: Int = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
                    level * 100 / scale
                }!!

                // Check if the battery percentage actually changed
                if (currentBatteryPercentLiveData.value != currentBatteryPercentLocal) {

                    // Post live data to update the UI
                    currentBatteryPercentLiveData.postValue(currentBatteryPercentLocal)

                    // Start the DataTransmissionService
                    sendMessageToService(context, "P:::$currentBatteryPercentLocal")
                }

                delay(batteryPercentDelay)
            }
        }
    }

    // Returns the current battery percentage
    fun getBatteryPercent(): LiveData<Int> {
        return currentBatteryPercentLiveData
    }


    // Get the current battery charging status
    //fun updateBatteryCharging(batteryStatus: Intent) {
    fun updateBatteryCharging(context: Context) {

        batteryChargingJob.cancel()

        batteryChargingJob = CoroutineScope(Dispatchers.IO).launch {

            while (true) {

                // Get the current battery status intent
                val batteryStatus: Intent? = IntentFilter(Intent.ACTION_BATTERY_CHANGED).let { ifilter ->
                    context.registerReceiver(null, ifilter)
                }

                val status: Int = batteryStatus?.getIntExtra(BatteryManager.EXTRA_STATUS, -1) ?: -1

                currentBatteryChargingLocal = status == BatteryManager.BATTERY_STATUS_CHARGING
                        || status == BatteryManager.BATTERY_STATUS_FULL

                // Check if the battery charging status actually changed
                if (currentBatteryChargingLiveData.value != currentBatteryChargingLocal) {

                    // Post live data to update the UI
                    currentBatteryChargingLiveData.postValue(currentBatteryChargingLocal)

                    // Start the DataTransmissionService
                    sendMessageToService(context, "C:::$currentBatteryChargingLocal")
                }

                delay(batteryChargingDelay)
            }
        }
    }

    // Returns the current battery charging status
    fun getBatteryCharging(): LiveData<Boolean> {
        return currentBatteryChargingLiveData
    }

    /*
    fun sendExistingNotifications(context: Context) {

        notificationJob.cancel()

        notificationJob = CoroutineScope(Dispatchers.IO).launch {

            while(true) {

                // Get the current notification manager
                val notificationManager =
                    context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

                // Get the active notifications
                val activeNotifications = notificationManager.activeNotifications

                // Send each notification app and count
                for (notification in activeNotifications) {
                    val appName = notification.packageName
                    val notificationCount =
                        activeNotifications.filter { it.packageName == appName }.size

                    // Send app name and count via Bluetooth DataTransmissionService
                    sendMessageToService(context, "N:::$appName,$notificationCount")
                }

                delay(notificationDelay)
            }
        }
    }

     */

}