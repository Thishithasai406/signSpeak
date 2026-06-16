<a id="signspeak"></a>

<p align="center">
  <img src="SignSpeak.png" alt="SignSpeak Banner" width="85%">
</p>

<h1 align="center">SignSpeak ✋</h1>
<p align="center">
  A Real-Time ASL Sign Language to Text and Speech Conversion Platform
  
<p align="center">
  <a href="https://drive.google.com/file/d/18ecXShPUJTx3V3qujCJZbQ_bQEhcN4w4/view?usp=sharing">
    <img src="https://img.shields.io/badge/▶%20Watch-Demo%20Video-red?style=for-the-badge" alt="Watch Demo">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python">
  <img src="https://img.shields.io/badge/Flask-3.x-000000?logo=flask">
  <img src="https://img.shields.io/badge/TensorFlow-2.13-FF6F00?logo=tensorflow">
  <img src="https://img.shields.io/badge/OpenCV-4.8-5C3EE8?logo=opencv">
  <img src="https://img.shields.io/badge/MediaPipe-0.10-4285F4?logo=google">
  <img src="https://img.shields.io/badge/CVZone-1.5.6-blue">
  <img src="https://img.shields.io/badge/license-MIT-green">
</p>

**SignSpeak** is an ASL sign language learning and recognition platform designed to make American Sign Language accessible to everyone. It combines a Flask-powered web interface for learning and practice with a real-time desktop recognition engine powered by computer vision, deep learning, and rule-based logic.

Built with Flask, TensorFlow, MediaPipe, and OpenCV, it performs **real-time ASL alphabet recognition (A–Z)**, enables **full sentence construction**, offers **spell-check suggestions**, and converts recognized text into **speech**.

**Local App** 👉 [http://localhost:5000](http://localhost:5000) *(after running `python app.py`)*


## Table of Contents

- [💡 About the Project](#about-the-project)
- [✨ Features](#features)
- [🗂️ Project Structure](#project-structure)
- [🖥️ Tech Stack](#tech-stack)
- [📄 Pages & Sections](#pages--sections)
- [🚀 Getting Started](#getting-started)
- [🧠 Model & Dataset](#model--dataset)
- [📝 Sentence Construction](#sentence-construction)
- [🔧 Troubleshooting](#troubleshooting)
- [🚀 Future Enhancements](#future-enhancements)
- [🤝 Contributing](#contributing)
- [🙏 Acknowledgements](#acknowledgements)
- [📜 License](#license)


---

## 💡 About the Project

**SignSpeak** is an end-to-end ASL fingerspelling platform that goes beyond single-letter detection. It enables **full sentence construction**, **word-level spell correction**, and **spoken output** — making it a practical communication tool, not just a classifier demo.


### What SignSpeak Does

- **Learners** explore all 26 ASL alphabet signs with images, descriptions, and interactive cards
- **Students** test their knowledge through practice quizzes with score tracking and streak counters
- **Users** perform real-time sign recognition via webcam — converting hand gestures into text and speech
- **Communicators** build complete sentences letter by letter, correct spelling with auto-suggestions, and speak the final message aloud


### The Core Idea

SignSpeak was built to bridge the gap between hearing and non-hearing communities by making ASL fingerspelling natural, engaging, and accessible. Instead of recognizing only isolated letters, the system is designed for real conversation:

1. Show a sign → get a letter prediction in real time
2. Confirm the letter with a **Next** gesture → it appends to your sentence
3. Add spaces between words, fix typos with **spell suggestions**, and hit **Speak** to hear the full sentence

This makes SignSpeak useful for spelling names, forming new words, and communicating vocabulary that may not exist as a dedicated ASL sign.


### Why Alphabet-Level Recognition Instead of Whole Words?

This project focuses on **individual ASL alphabet letters (A–Z)** rather than full ASL word recognition:

| Benefit | Description |
|---|---|
| **Beginner-friendly** | You only need to learn 26 hand signs |
| **More universal** | Fingerspelling is widely used in ASL for names, places, and new terms |
| **Any word can be formed** | Even unseen or new vocabulary can be spelled out |
| **Less data required** | Full-word ASL recognition needs massive datasets; alphabet-level works with ~4,680 images |
| **Sentence construction** | Letters combine into words and full sentences — enabling open-ended communication |

While alphabet-based communication is slower than full ASL vocabulary, it is the most **accessible, universal, and scalable** entry point for real-time sign-language interpretation.

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## ✨ Features

### Core AI Features

- Real-time ASL alphabet recognition (A–Z)
- 21-point hand landmark tracking via MediaPipe
- Skeleton rendering as CNN input
- CNN predicts gesture groups (0–7)
- Rule-based refinement to exact letters
- Sentence construction using gesture controls
- Spell suggestions using `pyenchant`
- Text-to-speech output using `pyttsx3`


### Website Features

- Learn Alphabets (A–Z) interactive section
- Practice mode with live webcam preview and real-time feedback
- Practice tests to evaluate user learning
- Score tracking, streak counters, and quiz completion feedback
- Clean and user-friendly web interface with smooth animations

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 🗂️ Project Structure

```
signSpeak-main/
│
├── app.py                         # Flask web server — serves UI, launches prediction engine
├── prediction.py                  # Core real-time ASL recognition logic (Tkinter + OpenCV + CNN)
├── cnn8grps_rad1_model.h5         # Pre-trained CNN model (8-group classifier)
├── requirements.txt               # Python dependencies (pinned versions)
├── prediction_errors.log          # Runtime error log (auto-generated)
│
├── templates/
│   └── index.html                 # SignSpeak web UI (Home, Learn, Practice, Live Preview)
│
├── static/                        # ASL alphabet sign images (A–Z) + background assets
│   ├── A.png … Z.png              # Per-letter hand sign reference images
│   └── background.png             # Hero section background
│
├── SignSpeak.png                  # Website preview banner
├── sign.png                       # ASL alphabet reference chart
├── handlandmark.png               # MediaPipe 21-point hand landmark diagram
└── Evaluation.png                 # Model evaluation results (group-level accuracy)
```

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 🖥️ Tech Stack

### Backend & AI

- **Web Framework**: [Flask](https://flask.palletsprojects.com/) — lightweight Python web server
- **Language**: Python 3.9+ (tested on Windows)
- **Deep Learning**: [TensorFlow 2.13](https://www.tensorflow.org/) + Keras — CNN model inference
- **Computer Vision**: [OpenCV](https://opencv.org/) — webcam capture and image processing
- **Hand Tracking**: [MediaPipe](https://mediapipe.dev/) + [CVZone](https://github.com/cvzone/cvzone) — 21-point landmark detection
- **Desktop GUI**: Tkinter + Pillow — live preview recognition window
- **Text-to-Speech**: [pyttsx3](https://pyttsx3.readthedocs.io/) — offline speech synthesis
- **Spell Checking**: [pyenchant](https://pyenchant.github.io/pyenchant/) — dictionary-based word suggestions


### Frontend

- **UI**: Single-page HTML/CSS/JavaScript (`templates/index.html`)
- **Styling**: Custom CSS with dark theme, gradients, and scroll animations
- **Assets**: Static PNG images for all 26 ASL alphabet signs


### Infrastructure

- **Process Management**: `subprocess` + optional `psutil` for prediction process tracking
- **Model Format**: Keras `.h5` (8-class softmax output)

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 📄 Pages & Sections

### Web Interface (`http://localhost:5000`)

| Section | Nav Link | Description |
|---|---|---|
| Home | Home | Hero banner, feature cards, and project story |
| Features | Features | Live recognition, learning, quizzes, UI, progress, design |
| About | About | Project inspiration and mission statement |
| Learn | Learn | Interactive A–Z alphabet grid with sign images and modal details |
| Practice | Practice | Quiz hub with mode selection and 10-question rounds |
| Live Preview | Camera Button | Launches `prediction.py` desktop app for real-time recognition |


### Learn Page

| Element | Description |
|---|---|
| Alphabet Grid | 26 clickable cards — each shows letter, sign image/emoji, and description modal |
| Letter Modal | Full sign image, letter name, and step-by-step sign description |


### Practice Page

| Mode | Description |
|---|---|
| Sign → Letter | Display a hand sign image; user picks the correct letter from 4 options |
| Letter → Sign | Display a letter; user picks the correct hand sign from 4 options |
| Quiz Complete | Trophy, final score, and performance message based on percentage |


### Live Preview Desktop App (`prediction.py`)

| Panel | Description |
|---|---|
| Camera Feed | Real-time mirrored webcam with hand skeleton overlay |
| Character Display | Currently detected letter (A–Z) |
| Sentence Builder | Accumulated text from confirmed gestures |
| Suggestions | Up to 4 spell-check word suggestions (click to apply) |
| Action Buttons | **Clear** (reset text) and **Speak** (text-to-speech output) |
| LIVE Badge | Real-time status indicator on camera panel |

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---



## 🚀 Getting Started

### Prerequisites

- Python `3.9` (recommended — TensorFlow 2.13 compatibility)
- A working **webcam**
- Windows (primary test platform; Linux/macOS may work with dependency adjustments)
- Git


### Step-by-Step Setup

**1. Clone the repository:**

```bash
git clone <repository-url>
cd signSpeak-main
```

**2. Create and activate a virtual environment:**

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
pip install flask
```

**4. Verify the model file is present:**

```
cnn8grps_rad1_model.h5   (~13 MB)
```

**5. Start the application:**

```bash
python app.py
```

**6. Open your browser at** `http://localhost:5000`

**7. Click the Live Preview camera button** to start real-time sign recognition.

Open [http://localhost:5000](http://localhost:5000) and click **Live Preview** to launch the real-time ASL recognition desktop window. 🚀

> **Note:** The first launch of Live Preview may take 15–30 seconds while TensorFlow loads the CNN model and initializes the webcam.

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 🧠 Model & Dataset

### Dataset

- **Name**: ASL Mediapipe Landmarked Dataset (A–Z)
- **Source**: [Kaggle — granthgaurav/asl-mediapipe-converted-dataset](https://www.kaggle.com/datasets/granthgaurav/asl-mediapipe-converted-dataset)
- **Classes**: 26 letters (A–Z) of American Sign Language fingerspelling
- **Samples per class**: 180 images per letter
- **Total Images**: ~4,681 (3,276 train / 702 validation / 703 test)
- **Input Size**: 400 × 400 × 3 skeleton-rendered images
- **Data format**: Hands pre-processed with MediaPipe — each image encodes 21 hand landmarks as a rendered skeleton on a white background


### Why 8 Groups Instead of 26 Direct Classes?

Certain ASL letters have **very similar hand shapes**. Training a 26-class CNN causes frequent misclassification within look-alike groups:

| Look-Alike Group | Letters |
|---|---|
| Fist variants | A, E, M, N, S, T |
| Open-hand variants | B, D, F, I, U, V, W, K, R |
| Curved hand | C, O |
| Index/thumb pairs | G, H |
| Single letter | L |
| Complex shapes | P, Q, Z |
| Crossed fingers | X |
| Extended shapes | Y, J |

**Solution:** Group 26 letters into **8 gesture categories**. The CNN classifies the group; **rule-based geometric logic** on MediaPipe landmarks determines the exact letter.

| Group | Letters in Group |
|---|---|
| 0 | A, E, M, N, S, T |
| 1 | B, D, F, I, U, V, W, K, R |
| 2 | C, O |
| 3 | G, H |
| 4 | L |
| 5 | P, Q, Z |
| 6 | X |
| 7 | Y, J |


#### Benefits of the 8-Group Approach

| Benefit | Description |
|---|---|
| **Higher Accuracy** | Model only separates 8 groups — easier learning, better performance |
| **Less Training Data** | 26-class training needs a much larger dataset; grouping works with ~4,680 images |
| **Reduces Misclassification** | Look-alike letters separated by geometric rules, not the CNN alone |
| **Faster & Stable Inference** | Less output complexity → faster training and real-time prediction |
| **Enables Rule Integration** | Joint locations allow distance/angle checks impossible with raw images alone |

> Once the CNN predicts the correct **group**, rule-based logic uses finger angles and distances to determine the **exact letter**.  
> **CNN (general shape) + Rules (fine differences) = best accuracy with limited data.**


### Why Skeleton Images Instead of Raw Hand Photos?

| Benefit | Description |
|---|---|
| **Background Independent** | Only hand pose is captured — no background, clothing, or lighting distractions |
| **Skin Tone Independent** | Performance does not depend on skin color — only joint geometry matters |
| **Higher Accuracy, Less Data** | ~4,680 skeleton images are enough; raw images would need 50,000+ samples |
| **Robust in Real-Time** | Works smoothly across different environments and camera quality |
| **Geometric Rule Integration** | Exact joint locations enable refinement of look-alike letters (M/N/S/T, U/V/W, G/H, P/Q/Z) |
| **Fast Training & Inference** | Smaller, meaningful input → quicker prediction → real-time performance |


### MediaPipe Hand Landmarks

MediaPipe detects and tracks **21 hand landmarks** per hand:

- **Landmark 0**: Wrist (base of hand)
- **Landmarks 1–4**: Thumb (CMC, MCP, IP, Tip)
- **Landmarks 5–8**: Index finger (MCP, PIP, DIP, Tip)
- **Landmarks 9–12**: Middle finger (MCP, PIP, DIP, Tip)
- **Landmarks 13–16**: Ring finger (MCP, PIP, DIP, Tip)
- **Landmarks 17–20**: Pinky finger (MCP, PIP, DIP, Tip)

Each landmark has normalized `(x, y, z)` coordinates used to:

1. Render the skeleton image fed into the CNN
2. Extract geometric features for rule-based letter refinement
3. Keep the system robust to background, lighting, and camera variations


### Model Training

| Parameter | Value |
|---|---|
| **Architecture** | Convolutional Neural Network (CNN) — TensorFlow + Keras |
| **Layers** | Convolution → Max-Pooling → Dense → Softmax (8 classes) |
| **Input** | 400 × 400 × 3 skeleton images |
| **Pre-processing** | Resize to 400×400, normalize pixels to 0–1 |
| **Loss** | Cross-entropy classification loss |
| **Metrics** | Top-1 accuracy, Top-3 accuracy, cross-entropy |
| **Output** | `cnn8grps_rad1_model.h5` — 8-group softmax classifier |
| **Data Split** | 80% train / 20% validation (group-level) |

```
Skeleton Image (400×400) → CNN → Group (0–7) → Rules → Letter (A–Z)
```


### Model Evaluation

![Evaluation Results](Evaluation.png)


### ASL Alphabet Reference

![ASL Alphabet A-Z](sign.png)


### MediaPipe Hand Landmarks Diagram

![Hand Landmarks](handlandmark.png)

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 📝 Sentence Construction

SignSpeak is built for **full sentence construction** — not just showing one letter at a time. Users spell words letter by letter, build complete sentences, fix spelling mistakes, and speak the result.


### Control Gestures

| Gesture | Action |
|---|---|
| **Next** | Confirm the current character and append it to the sentence |
| **Backspace** | Delete the last character from the sentence |
| **Pause / Double Space** | Insert a space character between words |

A temporal buffer of the **last 10 predictions** prevents accidental triggers from noisy frames. Implemented in `predict()` within `prediction.py`.


### How to Build a Sentence

1. **Show a hand sign** in front of the webcam
2. **See the predicted letter** displayed in real time on the Character panel
3. **Perform the Next gesture** to confirm and append the letter to your sentence
4. **Repeat** for each letter to spell out a word (e.g., H → E → L → L → O)
5. **Insert a space** using the pause/double-space gesture to move to the next word
6. **Use spell suggestions** — the last word is checked against a dictionary; up to 4 corrections are shown
7. **Click a suggestion** to replace the misspelled word instantly
8. **Hit Clear** to reset the entire sentence, or **Speak** to hear it aloud
9. **pyttsx3 reads the full sentence** — turning signed text into spoken communication


### Example Workflow

```
Sign "H" → Next → Sign "I" → Next → Pause (space) → Sign "T" → Next → Sign "H" → Next → Sign "E" → Next → Sign "R" → Next → Sign "E" → Next
Result: "HI THERE"
→ Apply spell suggestion if needed → Press Speak
```


### Full System Pipeline

```
Camera
  → MediaPipe (21 landmarks extracted)
  → CVZone (skeleton rendered on white background)
  → CNN Model (predicts gesture group 0–7)
  → Rule-Based Logic (refines to exact letter A–Z)
  → Sentence Builder (Next / Backspace / Space gestures)
  → Spell Suggestions (pyenchant dictionary check)
  → Text-to-Speech (pyttsx3 speaks the sentence)
```

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 🔧 Troubleshooting

| Issue | Solution |
|---|---|
| Camera not showing in Live Preview | Ensure no other app is using the webcam; close and relaunch Live Preview |
| Blank preview window | Check `prediction_errors.log` in the project root for runtime errors |
| `findHands` unpacking error | Use `cvzone==1.5.6` — with `draw=False`, `findHands()` returns a single list, not a tuple |
| Model not found | Place `cnn8grps_rad1_model.h5` in the project root (`signSpeak-main/`) |
| Slow first launch | Normal — TensorFlow model loading takes 15–30 seconds on first run |
| Spell suggestions not working | Install Enchant dictionaries: `pip install pyenchant` and ensure OS dictionary is available |

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 🚀 Future Enhancements

- 📱 Mobile / web-based recognition using TensorFlow Lite or WebAssembly
- 🤖 Direct landmark neural network (train on 3D coordinates instead of rendered skeletons)
- 🌍 Multi-language sign support (ISL, BSL, etc.)
- 🔄 Model fine-tuning on diverse lighting conditions and skin tones
- 🎬 Dynamic sign sequence recognition (words and phrases, not just letters)
- 🐳 Docker containerization for one-command deployment
- 🧪 Automated end-to-end testing with Playwright
- ☁️ Cloud deployment with browser-based webcam recognition (no desktop app required)

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 🙏 Acknowledgements

- [ASL Mediapipe Landmarked Dataset (A–Z)](https://www.kaggle.com/datasets/granthgaurav/asl-mediapipe-converted-dataset) — Training dataset by Granth Gaurav
- [MediaPipe](https://mediapipe.dev/) — Real-time hand landmark detection
- [CVZone](https://github.com/cvzone/cvzone) — Hand tracking wrapper and visualization
- [TensorFlow](https://www.tensorflow.org/) — Deep learning framework for CNN training and inference
- [OpenCV](https://opencv.org/) — Image capture, processing, and display
- [Flask](https://flask.palletsprojects.com/) — Web application framework
- [pyttsx3](https://pyttsx3.readthedocs.io/) — Offline text-to-speech engine
- [pyenchant](https://pyenchant.github.io/pyenchant/) — Spell checking and word suggestions

<p align="right">(<a href="#signspeak">⬆ Back to top</a>)</p>


---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*SignSpeak — bridging the gap between hearing and non-hearing communities through the universal language of gestures.*
