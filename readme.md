# 📘 AIML308 - Project 2

## 🎨 Multi-Style Visual Generation using Text-to-Image Diffusion Models

### 🕹️ For Game and Design Applications

_Semester 5 – B.Tech AI & ML_

---

## 🎯 Objective

This project aims to fine-tune a pretrained Stable Diffusion model on four distinct visual art styles frequently used in indie game development and digital design. The goal is to evaluate the model’s ability to generate high-quality visuals from well-crafted, style-specific text prompts.

---

## 📂 Dataset Plan

| 🖼️ Style Category     | 🗂️ Image Type                | 💬 Prompt Format Example                                                         |
| -------------------- | --------------------------- | ------------------------------------------------------------------------------- |
| 🎨 Pixel Art          | 32x32, 64x64 PNGs           | `A pixel art knight with a blue shield standing in a cave`                      |
| 🧙 Character Sketches | Pencil/line-art scans       | `A fantasy rogue with twin daggers in a sketch style, front pose`               |
| 📦 Isometric Scenes   | 2.5D digital illustrations  | `Isometric view of a wizard’s alchemy room with books and potions`              |
| 🌆 Room Layouts       | Top-down blueprints/layouts | `Top-down floor plan of a small library with reading areas and shelves labeled` |

---

## 🧠 Model Training

- **Base Model:** Stable Diffusion v1.5
- **Fine-tuning Method:** DreamBooth / LoRA (parameter-efficient fine-tuning)
- **Training Pipeline:** Image-caption dataset with custom prompt templates per style
- **Loss Function:** Cross Entropy + Perceptual Loss
- **Evaluation Metrics:**
  - CLIP Score (text-image alignment)
  - FID (Fréchet Inception Distance)
  - Human Preference Ranking

---

## 🛠️ Applications

- Asset generation for indie and 2D/3D games
- Style-consistent concept art generation
- Rapid prototyping for game levels and characters
- Procedural generation tools for creative workflows

---

## 📈 Results Overview

- Pixel Art style showed highest text-to-image alignment
- Sketches retained structure but required more training steps
- Isometric scenes achieved good spatial consistency
- Room layout generation worked best with labeled object prompts

---

## 📌 Limitations

- Struggles with highly complex prompts in small resolutions (e.g., 32x32)
- Requires multiple training iterations per style for optimal results
- Background blending is inconsistent for sketch inputs

---

## 🧳 Future Work

- Expand dataset diversity with dynamic lighting and environments
- Add support for animation (e.g., sprite generation or frame interpolation)
- Investigate mixed-style prompt blending and few-shot generalization
- Build a web-based visual interface for prompt testing and rendering

---

## 🏫 Academic Info

- **Course:** _AIML308 - Project 2_
- **Semester:** _5_
- **Degree:** _B.Tech Artificial Intelligence & Machine Learning_
- **Institution:** _Chandubhai S. Patel Institute of Technology_
- **Team Members:** _Aditya Patel, Kavya Prajapati_
- **Supervisor:** _Deep Mendha_

---

## 📜 License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for details.

---

## 🤝 Contributions

We welcome improvements and feedback, especially in the areas of:

- Data preprocessing and augmentation
- Prompt engineering
- Efficient fine-tuning strategies
- Evaluation metrics for style fidelity

---
