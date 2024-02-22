package com.example.smartglassesapp

import android.app.NotificationManager
import android.content.Context
import android.content.Intent
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import android.util.Log

class NotificationListener: NotificationListenerService() {

    /*
    override fun onCreate() {
        // Get the current notification manager
        //val notificationManager =
        //    applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // Get the active notifications
        //val activeNotifications = notificationManager.activeNotifications

        // Send each notification app and count
        sendMessageToService(applicationContext, activeNotifications.size.toString())
        for (notification in activeNotifications) {
            val appName = notification.packageName
            val notificationCount =
                activeNotifications.filter { it.packageName == appName }.size

            // Send app name and count via Bluetooth DataTransmissionService
            sendMessageToService(applicationContext, "N:::$appName,$notificationCount")
        }
    }

     */

    /*
    // This is called when a new notification is posted
    override fun onNotificationPosted(sbn: StatusBarNotification) {

        // Get app name
        val appName = sbn.packageName

        // Get the number of notifications from the app
        val activeNotifications = activeNotifications.filter { it.packageName == packageName }
        val notificationCount = activeNotifications.size

        // Send the app name and notification count via Bluetooth using DataTransmissionService
        sendMessageToService(applicationContext, "N:::$appName,$notificationCount")

    }

    // This is called when a notification is removed
    override fun onNotificationRemoved(sbn: StatusBarNotification) {

        // Get app name
        val appName = sbn.packageName

        // Get the number of notifications from the app
        val activeNotifications = activeNotifications.filter { it.packageName == appName }
        val notificationCount = activeNotifications.size

        // Send the app name and notification count via Bluetooth using DataTransmissionService
        sendMessageToService(applicationContext, "N:::$appName,$notificationCount")

    }

    // Send a message to the DataTransmissionService
    fun sendMessageToService(context: Context, message: String) {
        val serviceIntent = Intent(context, DataTransmissionService::class.java)
        serviceIntent.putExtra("message", message)
        context.startService(serviceIntent)
    }

     */

    override fun onListenerConnected() {
        super.onListenerConnected()
        Log.d(TAG, "Notification Listener connected")
        printNotifications()
    }

    override fun onNotificationPosted(sbn: StatusBarNotification) {
        super.onNotificationPosted(sbn)
        Log.d(TAG, "Notification posted: ${sbn.packageName}")
        printNotifications()
    }

    override fun onNotificationRemoved(sbn: StatusBarNotification) {
        super.onNotificationRemoved(sbn)
        Log.d(TAG, "Notification removed: ${sbn.packageName}")
        printNotifications()
    }

    private fun printNotifications() {
        val activeNotifications = activeNotifications
        val notificationCounts = mutableMapOf<String, Int>()

        for (sbn in activeNotifications) {
            val packageName = sbn.packageName
            notificationCounts[packageName] = notificationCounts.getOrDefault(packageName, 0) + 1
        }

        for ((packageName, count) in notificationCounts) {
            Log.d(TAG, "$packageName: $count")
        }
    }

    companion object {
        private const val TAG = "NotificationListener"
    }

}