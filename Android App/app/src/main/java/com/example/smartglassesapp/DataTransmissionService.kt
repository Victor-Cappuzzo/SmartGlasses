package com.example.smartglassesapp

import android.Manifest
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Binder
import android.os.Build
import android.os.IBinder
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import java.io.IOException
import java.io.OutputStream
import java.util.*
import java.util.concurrent.ConcurrentLinkedQueue
import kotlin.concurrent.fixedRateTimer

class DataTransmissionService: Service() {

    private val binder: IBinder = DataTransmissionBinder()
    private var isSending: Boolean = false
    private val messageQueue: Queue<String> = ConcurrentLinkedQueue()
    private val messageLock = Object()

    // Bluetooth variables
    private lateinit var bluetoothAdapter: BluetoothAdapter
    private lateinit var bluetoothSocket: BluetoothSocket
    private lateinit var outputStream: OutputStream
    private lateinit var bluetoothDevice: BluetoothDevice

    companion object {
        const val NOTIFICATION_ID = 1
        private const val NOTIFICATION_CHANNEL_ID = "DataTransmissionChannel"
        private const val NOTIFICATION_CHANNEL_NAME = "Data Transmission Channel"
    }

    inner class DataTransmissionBinder: Binder() {
        fun getService(): DataTransmissionService = this@DataTransmissionService
    }


    override fun onBind(intent: Intent?): IBinder? {
        return binder
    }


    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {

        /*
        if (intent?.action == "STOP_SERVICE") {
            stopForgroundService()
        }
        return START_STICKY

         */

        intent?.let {
            val message = intent.getStringExtra("message")
            message?.let {
                synchronized(messageLock) {
                    messageQueue.offer(message)
                    if (!isSending) {
                        isSending = true
                        sendNextMessage()
                    }
                }
            }
        }

        return START_NOT_STICKY
    }

    private fun sendNextMessage() {
        synchronized(messageLock) {
            if (messageQueue.isNotEmpty()) {
                val message = messageQueue.poll()
                SendMessageThread(message).start()
            }

            else {
                isSending = false

                // Stop the service when the queue is empty
                stopSelf()
            }
        }
    }

    fun addMessageToQueue(message: String) {
        messageQueue.offer(message)
        startForgroundService()
    }

    private fun startForgroundService() {
        if (!isSending && messageQueue.isNotEmpty()) {
            isSending = true
            createNotificationChannel()
            val notification: Notification = createNotification()
            startForeground(NOTIFICATION_ID, notification)

            fixedRateTimer(name = "DataTransmissionTimer", initialDelay = 0, period = 100) {
                synchronized(messageQueue) {
                    if (messageQueue.isNotEmpty()) {
                        val message = messageQueue.poll()
                        SendMessageThread(message).start()
                    }
                    else {
                        stopForgroundService()
                    }
                }
            }

        }
    }

    private fun stopForgroundService() {
        isSending = false
        stopForeground(true)
        stopSelf()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                NOTIFICATION_CHANNEL_ID,
                NOTIFICATION_CHANNEL_NAME,
                NotificationManager.IMPORTANCE_DEFAULT
            )
            val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(): Notification {
        val notificationBuilder = NotificationCompat.Builder(this, NOTIFICATION_CHANNEL_ID)
            .setContentTitle("Data Transmission")
            .setContentText("Transmitting data to PicoW")
            .setSmallIcon(R.drawable.ic_launcher_foreground)

        return notificationBuilder.build()
    }

    inner class SendMessageThread(val message: String): Thread() {
        override fun run() {

            // Set up bluetooth adapter
            bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()

            // Get all devices that are paired via bluetooth with the phone
            val pairedDevices: Set<BluetoothDevice>? = bluetoothAdapter.bondedDevices

            // Find the HC-06 board as the bluetooth device
            pairedDevices.let {
                for (device: BluetoothDevice in it!!) {

                    // Permissions check
                    if (ActivityCompat.checkSelfPermission(
                            applicationContext,
                            Manifest.permission.BLUETOOTH_CONNECT
                        ) != PackageManager.PERMISSION_GRANTED
                    ) {
                        return
                    }

                    // If the devices name is "HC-06", then set it as our device
                    if (device.name == "HC-06") {
                        bluetoothDevice = device
                        break
                    }
                }
            }

            try {
                // HC-06 UUID
                val uuid: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")

                // Permission check
                if (ActivityCompat.checkSelfPermission(
                        applicationContext,
                        Manifest.permission.BLUETOOTH_CONNECT
                    ) != PackageManager.PERMISSION_GRANTED
                ) {
                    return
                }

                // Set up and connect socket
                bluetoothSocket = bluetoothDevice.createRfcommSocketToServiceRecord(uuid)
                bluetoothSocket.connect()

                // Send the message to the HC-06
                outputStream = bluetoothSocket.outputStream
                outputStream.write((message + "\n").toByteArray())
                outputStream.flush()
                outputStream.close()
                bluetoothSocket.close()

            } catch (e: IOException) {
                e.printStackTrace()
            } finally {

                /*
                // Send next message in the queue
                synchronized(messageQueue) {
                    if (messageQueue.isNotEmpty()) {
                        val message = messageQueue.poll()
                        SendMessageThread(message).start()
                    }

                    else {
                        stopForgroundService()
                    }
                }

                 */

                sendNextMessage()
            }
        }
    }
}