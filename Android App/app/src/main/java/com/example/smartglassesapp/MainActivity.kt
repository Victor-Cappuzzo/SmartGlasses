package com.example.smartglassesapp

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.os.Message
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

class MainActivity : AppCompatActivity() {

    // Variable declaration
    private lateinit var bluetoothAdapter: BluetoothAdapter
    private lateinit var bluetoothSocket: BluetoothSocket
    private lateinit var outputStream: OutputStream
    private lateinit var bluetoothDevice: BluetoothDevice
    private lateinit var binding: ActivityMainBinding
    private var messageEditText: EditText? = null
    private var timeTextView: TextView? = null
    private var sendButton: Button? = null
    private var batteryTextView: TextView? = null
    private var chargingTextView: TextView? = null
    lateinit var model: AppViewModel

    private val messageQueue: Queue<String> = LinkedList()
    private var isSending: Boolean = false
    private val messageLock = Object()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Initialize view model
        model = ViewModelProvider(this).get(AppViewModel::class.java)

        // Variable initialization
        messageEditText = binding.messageEditText
        timeTextView = binding.timeTextView
        sendButton = binding.sendButton
        batteryTextView = binding.batteryTextView
        chargingTextView = binding.chargingTextView

        // Set up bluetooth adapter
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()

        // Get all devices that are paired via bluetooth with the phone
        val pairedDevices: Set<BluetoothDevice>? = bluetoothAdapter.bondedDevices

        // Find the HC-06 board as the bluetooth device
        pairedDevices.let {
            for (device: BluetoothDevice in it!!) {

                // Permissions check
                if (ActivityCompat.checkSelfPermission(
                        this,
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

        // Listen for if the send button is pressed
        sendButton!!.setOnClickListener {
            val message = messageEditText!!.text.toString()

            synchronized(messageLock) {
                // Add message to the queue
                messageQueue.offer("M:::$message")

                // Start sending if not already sending
                if (!isSending) {
                    isSending = true
                    sendNextMessage()
                }
            }
        }


        // Set observer for the current time and date value
        val dateTimeObserver = Observer<String> {newDateTime ->
                timeTextView!!.text = newDateTime

            synchronized(messageLock) {
                // Add message to the queue
                messageQueue.offer("T:::$newDateTime")

                // Start sending if not already sending
                if (!isSending) {
                    isSending = true
                    sendNextMessage()
                }
            }
            }
        model.getDateAndTime().observe(this, dateTimeObserver)

        // Start updating the date and time
        model.updateDateAndTime()


        // Set observer for the current battery percentage
        val batteryPercentObserver = Observer<Int> {newPercent ->
            batteryTextView!!.text = "$newPercent%"

            synchronized(messageLock) {
                // Add message to the queue
                messageQueue.offer("P:::$newPercent%")

                // Start sending if not already sending
                if (!isSending) {
                    isSending = true
                    sendNextMessage()
                }
            }
        }
        model.getBatteryPercent().observe(this, batteryPercentObserver)

        // Start updating the battery percentage
        model.updateBatteryPercent(applicationContext)


        // Set observer for the current battery charging status
        val batteryChargingObserver = Observer<Boolean> {isCharging ->

            // If the phone is charging
            if (isCharging) {
                chargingTextView!!.text = "ON"

                synchronized(messageLock) {
                    // Add message to the queue
                    messageQueue.offer("C:::ON")

                    // Start sending if not already sending
                    if (!isSending) {
                        isSending = true
                        sendNextMessage()
                    }
                }
            }

            // If the phone is not charging
            else {
                chargingTextView!!.text = "OFF"

                synchronized(messageLock) {
                    // Add message to the queue
                    messageQueue.offer("C:::OFF")

                    // Start sending if not already sending
                    if (!isSending) {
                        isSending = true
                        sendNextMessage()
                    }
                }
            }

        }
        model.getBatteryCharging().observe(this, batteryChargingObserver)

        // Start updating the battery charging status
        model.updateBatteryCharging(applicationContext)

    }

    // Sends the next message in the queue
    private fun sendNextMessage() {

        synchronized(messageLock) {

            // If there are messages in the queue
            if (messageQueue.isNotEmpty()) {
                val message = messageQueue.poll()

                // Start thread to send message
                SendMessageThread(message).start()
            }

            // If there are no more messages in the queue
            else {
                isSending = false
            }
        }
    }

    inner class SendMessageThread(val message: String): Thread() {
        override fun run() {
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

                // Display toast to indicate that data was send
                runOnUiThread {
                    Toast.makeText(applicationContext, "Message sent: $message", Toast.LENGTH_SHORT).show()
                }
            } catch (e: IOException) {
                e.printStackTrace()
            } finally {
                // Send next message in the queue
                sendNextMessage()
            }
        }
    }
}