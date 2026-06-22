# 🐔 Smart Poultry Farming with IoT and Machine Learning

An IoT-based smart poultry farming system that automates environmental monitoring, feeding, watering, cleaning, and disease detection. The project combines **ESP32**, **IoT sensors**, **Machine Learning**, and **Flask** to improve poultry farm management through real-time monitoring and intelligent automation.

---

## ✨ Features

* 🌡️ Real-time temperature and humidity monitoring
* 🌬️ Ammonia gas detection
* 💡 Automatic light control
* 🍽️ Automated feeding system
* 🚰 Automatic water dispensing
* 🧹 Automatic cleaning mechanism
* 🚨 Intrusion detection
* 🤖 AI-based poultry disease detection using CNN
* 📱 Telegram notifications for real-time alerts
* 📺 LCD display for live system status

---

## 🛠️ Technologies Used

### Hardware

* ESP32
* DHT11 Sensor
* MQ135 Gas Sensor
* LDR Sensor
* Ultrasonic Sensor
* Servo Motor
* DC Motors
* Relay Module
* Water Pump
* 16×2 I2C LCD

### Software

* Python
* Flask
* OpenCV
* TensorFlow
* Keras
* Arduino IDE
* Embedded C++

---

## 📂 Project Structure

```text
smart-poultry-farm/
│
├── firmware/          # ESP32 source code
├── software/          # Flask & Disease Detection
├── hardware/          # Circuit diagrams & components
├── images/            # Project images
├── documentation/     # Report & presentation
├── README.md
└── LICENSE
```

---

## ⚙️ System Workflow

1. ESP32 collects data from sensors.
2. Environmental conditions are monitored continuously.
3. Automatic actions are triggered based on sensor readings.
4. Farmers receive alerts through Telegram.
5. Users upload poultry images using the Flask web application.
6. The CNN model predicts whether the bird is healthy or diseased.
7. The prediction is displayed on the LCD and sent to the farmer.

---

## 📸 Screenshots

Add screenshots here after uploading them.

* Prototype
* Circuit Diagram
* Flask Web Application
* Disease Detection Output
* LCD Display

---

## 🚀 Future Enhancements

* Mobile application
* Cloud data storage
* Multi-disease classification
* Real-time camera detection
* Dashboard analytics

---

## 👨‍💻 Team

* S Madhu
* Preetha M
* Sahana Divatar
* Sandhya V

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ If you found this project helpful, please consider giving it a **Star**.
