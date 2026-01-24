# Bluetooth Presence Detection System - Proof of Concept

<div align="center">

**Real-time, privacy-preserving presence detection for adaptive soundscape systems**
**This system extends **CoSounds**, developed at natHACKS 2025, a complete reimagining of how students interact with adaptive soundscape systems.**

 [Documentation](https://drive.google.com/file/d/1aJjhq5XfcSvrsh3bxsnt4j4HbBal0YQZ/view?usp=sharing)

</div>

---

## 🎯 The Problem

The natHACKS 2025 CoSounds system used **timer-based presence tracking** with a 2-hour timeout. The problem? Timers detect entry but not departure.

**Consequences:**
- Students leaving early remain "present" → skews soundscape optimization
- Students staying longer get disconnected → manual reconnection required
- System operates on assumptions, not real occupancy data

**Real Impact:** If the system thinks 15 people are present but only 8 remain, it optimizes soundscapes for phantom preferences instead of actual students.

---

## 💡 The Solution

Replace timer assumptions with **automatic, real-time Bluetooth presence detection**. A Raspberry Pi continuously scans for registered devices within range. The Bluetooth signal radius naturally corresponds to room boundaries, creating an automatic geofence that accurately reflects who is actually present.

**Key Innovation:** NFC tap gating ensures students must explicitly opt-in before tracking begins—passive Bluetooth scanning alone does not create sessions.

---

## ✨ Features

- **🔐 Privacy-First Design** - No passive tracking; requires explicit NFC tap consent
- **⚡ Automatic Session Management** - PostgreSQL triggers handle entire lifecycle
- **🎯 Real-Time Detection** - Continuous Bluetooth scanning with 10-second intervals
- **⏱️ Grace Period System** - 15-minute buffer for brief absences (bathroom breaks, coffee runs)
- **📊 Built-in Analytics** - NumPy/Matplotlib for session statistics and visualization
- **🔄 Real-Time Dashboard** - React + Supabase subscriptions for live status updates
- **🛡️ Concurrent User Support** - Multiple students tracked independently without conflicts

---

## 🏗️ Architecture

<img width="651" height="428" alt="image" src="https://github.com/user-attachments/assets/0a1c013d-2a88-4124-b516-2b4820336585" />

### Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Django, Python, Django REST Framework |
| **Database** | Supabase PostgreSQL with Row Level Security |
| **Hardware** | Raspberry Pi 3 + Python Bleak |
| **Frontend** | React.js, Vite, TailwindCSS |
| **Analytics** | NumPy, Matplotlib |

---

## 🔄 How It Works

### 1️⃣ NFC Tap Check-In (Explicit Consent)

```
Student taps NFC tag 
  → System sets tap_flag = true in database
  → Raspberry Pi continuously scans for Bluetooth devices
  → Django creates session ONLY when:
      ✓ tap_flag == true 
      ✓ AND device detected
  → tap_flag resets to false (single-use)
  → Device status → "connected"
```

### 2️⃣ Automatic Tracking

Once checked in, the system monitors device presence:
- **30-second detection timeout** - Accommodates signal fluctuations
- **15-minute grace period** - Handles brief absences without re-authentication
- **PostgreSQL triggers** - Automatically manage session lifecycle

### 3️⃣ Automatic Departure

```
Device leaves Bluetooth range
  → System enters 30-second timeout
  → Grace period begins (15 minutes)
  → If device doesn't return:
      → Trigger fires: end_sessions_on_grace_period
      → Session ends with accurate timestamp
```

### Session States

| State | Description |
|-------|-------------|
| `connected` | Device actively detected with valid NFC tap |
| `disconnected` | Device not in range or session ended |
| `grace_period` | Temporary buffer before marking disconnected |

---



## 🔬 Context



CoSounds replaces multi-step feedback (QR codes, apps, surveys) with **instant NFC tap interaction**. Students vote in real-time using physical Green/Red NFC tags. The ML pipeline uses Environmental Sound Classification (ESC-50 dataset) with collective utility optimization to aggregate individual preferences into a single coherent soundscape for shared spaces.

### Why Presence Detection Matters

Accurate presence detection enables:
- ✅ Precise entry/exit timestamps for behavioral research
- ✅ Correlation between soundscape preferences and time-of-day
- ✅ Group study dynamics pattern analysis
- ✅ Real-time occupancy analytics
- ✅ Proper aggregation of only currently present students

---

## 🐛 Known Limitations & Solutions

MAC address randomization on modern devices and lack of iOS web Bluetooth support present challenges for client-side implementations, but this is a backend presence detection system where devices are pre-registered in the database. Future work includes developing a native mobile app for automatic device registration that detects MAC addresses during onboarding, eliminating manual registration and supporting both iOS and Android platforms with proper Bluetooth permissions.

---

## 🔮 Future Enhancements

- [ ] **Native Mobile App** - Automatic device registration with MAC address detection
- [ ] **BLE Beacon Integration** - Enhanced positioning with Bluetooth Low Energy beacons
- [ ] **Differential Privacy** - Enhanced privacy controls for sensitive data
- [ ] **Export Functionality** - CSV/Excel reports for administrators and researchers

---

### Resources

- 🎨 [CoSounds on Devpost](https://devpost.com/software/cosounds)
- 💻 [GitHub Repository](https://github.com/Pranav-Talwar/Cosound)
- 📊 [Cosounds Pitch Deck]()
- 🔬 [MSL Official Website](https://sites.google.com/ualberta.ca/msl)

---

<div align="center">

**Project Status:** ✅ Functional Proof of Concept - Core Features Implemented and Tested

Made with ❤️ for better learning environments

</div>
