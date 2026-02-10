# Real-Time Finger-Controlled Tic Tac Toe with AI

A computer vision–based interactive game controlled using hand tracking and gesture recognition.  
This project demonstrates real-time image processing, event-driven logic, and AI decision-making.

---

## 🔍 Project Description

This system uses a webcam to detect hand landmarks via MediaPipe and allows the user to interact with a Tic Tac Toe board without physical input devices.

A move is registered after holding the index finger over a grid cell for 3 seconds.  
An AI opponent responds using a rule-based decision algorithm.

---

## 🧠 Technical Highlights

- Real-time hand landmark detection (MediaPipe)
- Coordinate mapping from normalized space to pixel space
- Hover-based gesture interaction system
- Circular animated visual timer
- AI move selection logic (Win → Block → Random)
- Winner detection algorithm
- Event-driven game state management

---

## 🛠 Technologies

- Python
- OpenCV
- MediaPipe
- NumPy

---

## 🧩 System Architecture

1. Webcam frame capture  
2. Hand landmark detection  
3. Fingertip coordinate extraction  
4. Grid cell mapping  
5. Hover-time validation  
6. Board state update  
7. AI decision execution  
8. Winner evaluation  

---

## ▶ Installation

```bash
pip install opencv-python mediapipe numpy
