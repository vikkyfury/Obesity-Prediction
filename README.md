# Obesity Prediction Project

A machine learning project that predicts obesity risk levels using various health and lifestyle factors. This project includes both the model development (Jupyter notebooks) and a web application for real-time predictions.

## 🎯 Problem Statement

Develop a multi-class prediction model to assess obesity risk, focusing on its association with cardiovascular disease. The model predicts one of seven obesity categories based on various health and lifestyle factors.

## 📊 Features

The model uses the following features to predict obesity risk:

- **id** – Person Number
- **Gender** - Person gender (Male/Female)
- **Age** – Age of the person
- **Height** – Height of the person (in meters)
- **Weight** – Weight of the person (in kg)
- **Family_history_with_overweight** – Is there any person in family with overweight
- **FAVC** – Frequent consumption of high caloric food
- **FCVC** – Frequency of vegetables consumption
- **NCP** – Number of main meals
- **CAEC** – Consumption of food between meals
- **SMOKE** – Smoking status
- **CH2O** – Water consumption per day
- **SCC** – Calories monitoring
- **FAF** – Physical activity frequency
- **TUE** – Time using technology devices
- **CALC** – Alcohol consumption
- **MTRANS** – Mode of transportation

## 🎯 Output Categories

The model predicts one of the following obesity categories:

- **0**: Insufficient Weight
- **1**: Normal Weight
- **2**: Overweight Level I
- **3**: Overweight Level II
- **4**: Obesity Type I
- **5**: Obesity Type II
- **6**: Obesity Type III

## 🏗️ Project Structure

```
Obesity-Prediction/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
├── notebooks/               # Jupyter notebooks for model development
│   └── DIC_final.ipynb     # Main analysis notebook
├── models/                  # Trained model files
│   └── my_model_nn_1.h5    # Neural network model
├── web_app/                 # Flask web application
│   ├── app.py              # Main Flask application
│   ├── templates/          # HTML templates
│   │   ├── full.html      # Input form
│   │   └── output.html    # Results page
│   └── static/            # Static files (CSS, JS, images)
├── data/                   # Dataset files
├── docs/                   # Documentation
│   └── DIC_final_report.pdf # Project report
└── tests/                  # Unit tests (to be added)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Obesity-Prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the web application:
```bash
cd web_app
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## 📈 Model Performance

We evaluated multiple machine learning models:

- **Neural Network** (Selected for deployment)
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Naive Bayes
- Support Vector Machine (SVM)

The neural network model showed the best performance and was selected for the web application.

## 🌐 Web Application

The Flask web application provides a user-friendly interface for obesity risk prediction:

- **Input Form**: Collects all required health and lifestyle parameters
- **Real-time Prediction**: Returns obesity risk category instantly
- **Responsive Design**: Works on desktop and mobile devices

### Features:
- Clean, modern UI
- Form validation
- Error handling
- Mobile-responsive design

## 📚 Usage

1. **Model Development**: Use the Jupyter notebook in `notebooks/` to explore the data and develop new models
2. **Web Application**: Run the Flask app to get real-time predictions
3. **API**: The Flask app can be extended to provide API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name/Team Name

## 🙏 Acknowledgments

- Dataset providers
- Open source community
- Academic institutions

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This is a research project and should not be used as the sole basis for medical decisions. Always consult healthcare professionals for medical advice.

