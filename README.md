# HandSync

HandSync is a 3D-printed robotic hand controlled via Python and Arduino, designed to replicate human hand movements detected through a camera using OpenCV and serial communication.

---

## How It Works

1. **Serial Port Setup**  
   The Python script will prompt you to select the correct serial port (the one connected to the Arduino). If you're unsure, it will help you identify the right one.

2. **Hand Position Detection**  
   The camera activates and begins tracking your hand using the MediaPipe framework. By calculating the angles between key hand landmarks, it estimates the positions of the fingers and wrist.

3. **Arduino Control**  
   The detected joint angles are sent to the Arduino via serial communication, which maps them to the corresponding servo motor positions to replicate hand movements.

---

## Key Features

- **Accurate Detection:** Joint angles are detected precisely, regardless of the distance from the camera (as long as MediaPipe can detect your hand).
- **Orientation Flexibility:** The system can accurately replicate hand movements even if the forearm is rotated or the hand is upside down.
- **Functional Grip:** The joints are designed to have enough strength to handle small objects.

---

## Known Limitations

- No wrist mounting system is currently available.
- Requires a wired connection to the computer for serial communication (no wireless support yet).
- The PLA 3D-printed fingers may lack sufficient grip strength.
- Elastic bands may overstretch over time, affecting performance.

## Future Improvements

- Replace elastics with springs for better durability.
- Strengthen the mounting system for improved stability.
- Implement wireless communication for greater flexibility.
