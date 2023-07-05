package com.example.smartglassesapp

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.*
import java.lang.Math.abs
import java.text.SimpleDateFormat
import java.util.*

class AppViewModel: ViewModel() {

    // Variable declarations
    private val currentDateTimeLiveData = MutableLiveData<String>()
    private var currentDateTimeLocal = ""
    private var currentTime: Long = 0
    private val sdf = SimpleDateFormat("'Date\n'dd-MM-yyyy '\n\nand\n\nTime\n'HH:mm:ss z")

    private lateinit var viewModelJob: Job
    private lateinit var ioScope: CoroutineScope
    private val updateTime: Long = 1000

    init {
        viewModelJob = Job()
        ioScope = CoroutineScope(Dispatchers.IO + viewModelJob)
        currentTime = Date().time
    }

    // Get the current date and time, and keep these values updated
    fun updateDateAndTime() {

        // Cancel the job object in case the user wants to start it again
        viewModelJob.cancel()

        // Launch returns a Job object that w can then use to cancel the coroutine
        viewModelJob = CoroutineScope(Dispatchers.IO).launch {

            // Start async process
            async {

                // Run this loop infinitely
                while (true) {

                    // Get current time
                    var tempTime: Long = Date().time

                    // Check if we need to update the date and time
                    if (abs(tempTime - currentTime) < updateTime) {

                        // Update the date and time
                        currentTime = tempTime
                        currentDateTimeLocal = sdf.format(Date())
                        currentDateTimeLiveData.postValue(currentDateTimeLocal)

                        // Update on UI thread
                        withContext(Dispatchers.Main) {
                            getDateAndTime()
                        }

                    }
                }
            }
        }

    }

    // Returns the current date and time
    fun getDateAndTime(): LiveData<String> {
        return currentDateTimeLiveData
    }

}