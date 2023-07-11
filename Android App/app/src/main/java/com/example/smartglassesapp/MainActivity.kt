package com.example.smartglassesapp

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
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
    lateinit var model: AppViewModel

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
                    // TODO: Consider calling
                    //    ActivityCompat#requestPermissions
                    // here to request the missing permissions, and then overriding
                    //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                    //                                          int[] grantResults)
                    // to handle the case where the user grants the permission. See the documentation
                    // for ActivityCompat#requestPermissions for more details.
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

        // Start thread to send messages
        SendMessageThread("M:::$message").start()
    }

    // Set observer for the current time and date value
    val dateTimeObserver = Observer<String> {newDateTime ->
            timeTextView!!.text = newDateTime
            SendMessageThread("T:::$newDateTime").start()
        }

        model.getDateAndTime().observe(this, dateTimeObserver)

        model.updateDateAndTime(timeTextView!!)

        /*
        // Update date and time
        //model.updateDateAndTime()
        model.updateDateAndTime { message ->
            SendMessageThread(message).start()
        }

        // Set observer for the current date/time
        val dateTimeObserver = Observer<String> {newDateTime ->
            SendMessageThread(newDateTime).start()
        }

        // Set the dateTimeObserver to changes in the date and time
        model.getDateAndTime().observe(this, dateTimeObserver)

         */

    }

    inner class SendMessageThread(val message: String): Thread() {
        override fun run() {
            try {
                // HC-06 UUID
                val uuid: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")

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
            }
        }
    }
}