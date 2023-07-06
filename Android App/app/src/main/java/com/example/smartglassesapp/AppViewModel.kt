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
import kotlin.coroutines.CoroutineContext
import kotlin.coroutines.coroutineContext

class AppViewModel: ViewModel() {

    // Variable declarations
    private val currentDateTimeLiveData = MutableLiveData<String>()
    private var currentDateTimeLocal = ""
    private var currentTime: Long = 0
    private val sdf = SimpleDateFormat("Date dd-MM-yyyy Time HH:mm:ss z")

    private val updateTime: Long = 1000
    private var viewModelJob: Job = Job()
    //private lateinit var ioScope: CoroutineScope
    private val coroutineContext: CoroutineContext
        get() = viewModelJob + Dispatchers.Main

    // Get the current date and time, and keep these values updated
    fun updateDateAndTime(callback: (String) -> Unit) {

        viewModelJob.cancel()

        viewModelJob = CoroutineScope(coroutineContext).launch {

            while (true) {
                val currentDateTime = sdf.format(Date())
                currentDateTimeLiveData.postValue((currentDateTime))
                callback(currentDateTime) // Pass the message back to MainActivity
                delay(updateTime)
            }
        }

    }

    // Returns the current date and time
    fun getDateAndTime(): LiveData<String> {
        return currentDateTimeLiveData
    }

}