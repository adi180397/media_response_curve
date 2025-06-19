# 📈 Media Response Curve Tool

A powerful and interactive **Streamlit web app** designed to help small and medium businesses understand how their **marketing spend translates into response/output** using well-established mathematical models like **adstocking**, **Hill saturation**, and **response elasticity**.

---

## 🔧 What This Tool Does

* Upload real-world **media spend data**
* Apply **adstock transformation** to account for media decay
* Use **Hill saturation function** to model diminishing returns
* Highlight critical curve points:

  * **A: Inflection** (response accelerates)
  * **C: Diminishing Return** (response slows down)
  * **D: Saturation** (response plateaus)
* Compute and plot **response elasticity** to guide spend decisions
* Support campaign-level selection
* Deployed freely via **Streamlit Cloud**

---

## 📅 Mathematical Formulation

### 1. ✨ Adstock Transformation

Accounts for carry-over effect of media:

$$
Adstock_t = Spend_t + \lambda \cdot Adstock_{t-1}
$$

Where:

* $\lambda = 0.5^{\frac{1}{\text{Half-life}}}$

### 2. ↗ Saturation Function (Hill Function)

Models the diminishing return:

$$
Saturation(x) = \frac{x^p}{x^p + Penetration^p}
$$

Where:

* $x$ is adstocked spend
* $p$ is the **Hill exponent** (steepness of curve)
* **Penetration** defines when the curve starts flattening

### 3. 📊 Response Calculation

$$
Response = Effectiveness \times Saturation(Adstock)
$$

### 4. 📂 Elasticity (Responsiveness to Spend)

$$
Elasticity = \frac{dY}{dX} \cdot \frac{X}{Y}
$$

Where:

* $\frac{dY}{dX}$ is the slope of the curve
* Shows how much % gain in response you get for 1% increase in spend

### Elasticity Zones:

| Elasticity | Interpretation            | Spend Recommendation |
| ---------- | ------------------------- | -------------------- |
| > 1        | High efficiency           | Increase spend       |
| = 1        | Proportional              | Maintain spend       |
| 0.5 to 1   | Diminishing return begins | Monitor or optimize  |
| < 0.5      | Poor ROI zone             | Reduce or reallocate |
| \~ 0       | Saturated                 | Stop spending        |

---

## 📊 Features

* Interactive campaign selection
* Input control over:

  * Half-life (days)
  * Penetration (flattening point)
  * Effectiveness (scale)
  * Hill power (curve steepness)
* Plots:

  * Response Curve
  * Points A, C, D
  * Elasticity Curve (optional toggle)
* Upload your own CSV files
* View adstocked spend, model response, and elasticity in table format

---

## 📁 CSV Input Format

| Date       | Campaign | Spend | Sales (optional) |
| ---------- | -------- | ----- | ---------------- |
| 2024-01-01 | TV       | 1000  | 120              |
| 2024-01-02 | TV       | 1500  | 140              |
| ...        | ...      | ...   | ...              |

---

## 🚀 Deploying It Yourself (Optional)

### Requirements:

```txt
streamlit
pandas
numpy
matplotlib
```

### Local Run:

```bash
streamlit run app.py
```

### Free Hosting:

* Push code to GitHub
* Deploy via [https://streamlit.io/cloud](https://streamlit.io/cloud)

---

## 🌟 Author

**Aditya Kumar**
Market Mix Modeling | Data Analyst | IIT Delhi (TRIPP)
Feel free to connect or contribute!

---

## 🎨 Screenshot (Optional)

Add one here to show the output.

---

## 💊 Future Improvements

* Add ROI over time
* MMM model integration
* Budget simulation tool
* Downloadable reports

---

*"A great tool to bring data-driven media investment insights to even small and medium-sized businesses."*
