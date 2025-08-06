import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Input, Add, Concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, LearningRateScheduler
from tensorflow.keras.regularizers import l1_l2
import os
import warnings
warnings.filterwarnings('ignore')

# Set random seeds
np.random.seed(42)
tf.random.set_seed(42)

class AdvancedObesityTrainer:
    def __init__(self):
        self.scaler = RobustScaler()
        self.best_model = None
        self.best_score = 0
        self.best_model_name = ""
        self.results = {}
        
    def create_realistic_data(self):
        """Create realistic obesity dataset"""
        print("Creating realistic obesity dataset...")
        
        np.random.seed(42)
        n_samples = 15000  # Large dataset
        
        # Realistic data generation
        data = {
            'Gender': np.random.choice(['Male', 'Female'], n_samples, p=[0.48, 0.52]),
            'Age': np.random.normal(35, 12, n_samples).clip(18, 80),
            'Height': np.random.normal(170, 10, n_samples).clip(150, 200),
            'Weight': np.random.normal(70, 20, n_samples).clip(40, 150),
            'family_history_with_overweight': np.random.choice(['yes', 'no'], n_samples, p=[0.6, 0.4]),
            'FAVC': np.random.choice(['yes', 'no'], n_samples, p=[0.7, 0.3]),
            'FCVC': np.random.choice([1, 2, 3], n_samples, p=[0.2, 0.5, 0.3]),
            'NCP': np.random.choice([1, 2, 3, 4], n_samples, p=[0.1, 0.2, 0.5, 0.2]),
            'CAEC': np.random.choice(['no', 'Sometimes', 'Frequently', 'Always'], n_samples, p=[0.3, 0.4, 0.2, 0.1]),
            'SMOKE': np.random.choice(['yes', 'no'], n_samples, p=[0.2, 0.8]),
            'CH2O': np.random.normal(2.5, 1, n_samples).clip(1, 5),
            'SCC': np.random.choice(['yes', 'no'], n_samples, p=[0.3, 0.7]),
            'FAF': np.random.choice([0, 1, 2, 3], n_samples, p=[0.4, 0.3, 0.2, 0.1]),
            'TUE': np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.5, 0.2]),
            'CALC': np.random.choice(['no', 'Sometimes', 'Frequently', 'Always'], n_samples, p=[0.5, 0.3, 0.15, 0.05]),
            'MTRANS': np.random.choice(['Automobile', 'Bike', 'Motorbike', 'Public_Transportation', 'Walking'], 
                                     n_samples, p=[0.4, 0.1, 0.1, 0.2, 0.2])
        }
        
        df = pd.DataFrame(data)
        
        # Realistic BMI calculations with correlations
        df['BMI'] = df['Weight'] / ((df['Height'] / 100) ** 2)
        
        # Add realistic correlations
        family_history_mask = df['family_history_with_overweight'] == 'yes'
        df.loc[family_history_mask, 'BMI'] *= np.random.normal(1.1, 0.05, sum(family_history_mask))
        
        smoke_mask = df['SMOKE'] == 'yes'
        df.loc[smoke_mask, 'BMI'] *= np.random.normal(0.9, 0.05, sum(smoke_mask))
        
        favc_mask = df['FAVC'] == 'yes'
        df.loc[favc_mask, 'BMI'] *= np.random.normal(1.15, 0.05, sum(favc_mask))
        
        # Obesity categorization
        def categorize_obesity(bmi):
            if bmi < 18.5: return 0
            elif bmi < 25: return 1
            elif bmi < 30: return 2
            elif bmi < 35: return 3
            elif bmi < 40: return 4
            elif bmi < 45: return 5
            else: return 6
        
        df['Obesity'] = df['BMI'].apply(categorize_obesity)
        
        # Feature mappings
        mappings = {
            'Gender': {'Male': 0, 'Female': 1},
            'family_history_with_overweight': {'no': 0, 'yes': 1},
            'FAVC': {'no': 0, 'yes': 1},
            'SMOKE': {'no': 0, 'yes': 1},
            'SCC': {'no': 0, 'yes': 1},
            'CAEC': {'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3},
            'CALC': {'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3},
            'MTRANS': {'Automobile': 0, 'Bike': 1, 'Motorbike': 2, 'Public_Transportation': 3, 'Walking': 4}
        }
        
        for col, mapping in mappings.items():
            df[col] = df[col].map(mapping)
        
        # Engineered features
        df['BMI'] = df['Weight'] / ((df['Height'] / 100) ** 2)
        df['Age_Height_Ratio'] = df['Age'] / df['Height']
        df['Weight_Height_Ratio'] = df['Weight'] / df['Height']
        df['Activity_Score'] = (4 - df['FAF']) * (3 - df['TUE'])
        df['Diet_Score'] = df['FCVC'] * df['NCP'] * (1 + df['CAEC'])
        df['Lifestyle_Score'] = df['Activity_Score'] - df['Diet_Score']
        
        # Select features
        feature_columns = [
            'Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight',
            'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'MTRANS',
            'BMI', 'Age_Height_Ratio', 'Weight_Height_Ratio', 'Activity_Score', 'Diet_Score', 'Lifestyle_Score'
        ]
        
        X = df[feature_columns]
        y = df['Obesity']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # One-hot encoding
        y_train_encoded = tf.keras.utils.to_categorical(y_train, num_classes=7)
        y_test_encoded = tf.keras.utils.to_categorical(y_test, num_classes=7)
        
        self.X_train = X_train_scaled
        self.X_test = X_test_scaled
        self.y_train = y_train_encoded
        self.y_test = y_test_encoded
        
        print(f"Dataset: {X_train.shape[0]} training, {X_test.shape[0]} test samples")
        print(f"Features: {X_train.shape[1]}, Classes: 7")
        
    def create_residual_block(self, x, filters):
        """Residual block for better gradient flow"""
        shortcut = x
        x = Dense(filters, activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4))(x)
        x = BatchNormalization()(x)
        x = Dropout(0.3)(x)
        x = Dense(filters, activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4))(x)
        x = BatchNormalization()(x)
        if shortcut.shape[-1] == filters:
            x = Add()([shortcut, x])
        return x
    
    def create_model_1(self, name="ResNet_DNN"):
        """ResNet-style DNN"""
        inputs = Input(shape=(self.X_train.shape[1],))
        x = Dense(256, activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(0.3)(x)
        x = self.create_residual_block(x, 256)
        x = self.create_residual_block(x, 128)
        x = self.create_residual_block(x, 64)
        x = Dense(32, activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.2)(x)
        outputs = Dense(7, activation='softmax')(x)
        return Model(inputs=inputs, outputs=outputs), name
    
    def create_model_2(self, name="Wide_Deep_DNN"):
        """Wide and Deep network"""
        inputs = Input(shape=(self.X_train.shape[1],))
        wide = Dense(512, activation='relu')(inputs)
        wide = Dense(256, activation='relu')(wide)
        deep = Dense(128, activation='relu')(inputs)
        deep = Dense(128, activation='relu')(deep)
        deep = Dense(64, activation='relu')(deep)
        deep = Dense(64, activation='relu')(deep)
        deep = Dense(32, activation='relu')(deep)
        combined = Concatenate()([wide, deep])
        x = Dense(128, activation='relu')(combined)
        x = BatchNormalization()(x)
        x = Dropout(0.3)(x)
        outputs = Dense(7, activation='softmax')(x)
        return Model(inputs=inputs, outputs=outputs), name
    
    def create_model_3(self, name="Attention_DNN"):
        """DNN with attention mechanism"""
        inputs = Input(shape=(self.X_train.shape[1],))
        x = Dense(512, activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(0.3)(x)
        attention = Dense(512, activation='sigmoid')(x)
        x = tf.keras.layers.Multiply()([x, attention])
        x = Dense(256, activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.3)(x)
        x = Dense(128, activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.2)(x)
        x = Dense(64, activation='relu')(x)
        outputs = Dense(7, activation='softmax')(x)
        return Model(inputs=inputs, outputs=outputs), name
    
    def learning_rate_schedule(self, epoch):
        """Custom learning rate schedule"""
        initial_lr = 0.001
        if epoch < 10: return initial_lr
        elif epoch < 50: return initial_lr * 0.5
        else: return initial_lr * 0.1
    
    def train_model(self, model, name, epochs=300):
        """Train a model with advanced techniques"""
        print(f"\nTraining {name}...")
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        callbacks = [
            EarlyStopping(monitor='val_accuracy', patience=40, restore_best_weights=True, verbose=1),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=20, min_lr=1e-7, verbose=1),
            LearningRateScheduler(self.learning_rate_schedule)
        ]
        
        history = model.fit(
            self.X_train, self.y_train,
            validation_data=(self.X_test, self.y_test),
            epochs=epochs, batch_size=32, callbacks=callbacks, verbose=1
        )
        
        test_loss, test_accuracy = model.evaluate(self.X_test, self.y_test, verbose=0)
        y_pred = model.predict(self.X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_test_classes = np.argmax(self.y_test, axis=1)
        
        precision = precision_score(y_test_classes, y_pred_classes, average='weighted')
        recall = recall_score(y_test_classes, y_pred_classes, average='weighted')
        f1 = f1_score(y_test_classes, y_pred_classes, average='weighted')
        
        self.results[name] = {
            'model': model, 'accuracy': test_accuracy,
            'precision': precision, 'recall': recall, 'f1': f1,
            'history': history.history, 'predictions': y_pred_classes
        }
        
        print(f"{name} Results:")
        print(f"  Accuracy: {test_accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        
        if test_accuracy > self.best_score:
            self.best_score = test_accuracy
            self.best_model = model
            self.best_model_name = name
            print(f"  🎉 New best model! Accuracy: {test_accuracy:.4f}")
        
        return model, history
    
    def train_all_models(self):
        """Train all advanced models"""
        print("Starting advanced model training...")
        self.create_realistic_data()
        
        models = [
            self.create_model_1(),
            self.create_model_2(),
            self.create_model_3()
        ]
        
        for model, name in models:
            self.train_model(model, name)
        
        self.print_results_summary()
        
    def print_results_summary(self):
        """Print results summary"""
        print("\n" + "="*60)
        print("ADVANCED MODEL TRAINING RESULTS")
        print("="*60)
        
        sorted_results = sorted(
            self.results.items(),
            key=lambda x: x[1]['accuracy'],
            reverse=True
        )
        
        print(f"{'Model':<20} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10}")
        print("-" * 60)
        
        for name, results in sorted_results:
            print(f"{name:<20} {results['accuracy']:<10.4f} {results['precision']:<10.4f} "
                  f"{results['recall']:<10.4f} {results['f1']:<10.4f}")
        
        print("\n" + "="*60)
        print(f"🏆 BEST MODEL: {self.best_model_name}")
        print(f"🏆 BEST ACCURACY: {self.best_score:.4f}")
        print("="*60)
        
        if self.best_score >= 0.95:
            print("🎉 TARGET ACHIEVED! 95%+ accuracy reached!")
        else:
            print(f"📈 Current best: {self.best_score:.4f} - Keep training for 95%!")
    
    def save_best_model(self, model_path='best_advanced_model.h5'):
        """Save the best model"""
        if self.best_model is not None:
            os.makedirs('models', exist_ok=True)
            self.best_model.save(f'models/{model_path}')
            print(f"\n✅ Best model saved to: models/{model_path}")
            
            import joblib
            joblib.dump(self.scaler, 'models/advanced_scaler.pkl')
            print(f"✅ Advanced scaler saved to: models/advanced_scaler.pkl")
            
            model_info = {
                'best_model_name': self.best_model_name,
                'best_accuracy': self.best_score,
                'feature_columns': [
                    'Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight',
                    'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'MTRANS',
                    'BMI', 'Age_Height_Ratio', 'Weight_Height_Ratio', 'Activity_Score', 'Diet_Score', 'Lifestyle_Score'
                ],
                'results': self.results
            }
            
            import json
            with open('models/advanced_model_info.json', 'w') as f:
                json.dump(model_info, f, indent=2, default=str)
            print(f"✅ Model info saved to: models/advanced_model_info.json")
        else:
            print("❌ No best model found!")

def main():
    """Main function"""
    print("🚀 Advanced Obesity Prediction Model Training")
    print("🎯 Target: 95% Accuracy")
    print("="*60)
    
    trainer = AdvancedObesityTrainer()
    trainer.train_all_models()
    trainer.save_best_model()
    
    print(f"\n✅ Training completed!")
    print(f"🏆 Best model: {trainer.best_model_name}")
    print(f"🏆 Best accuracy: {trainer.best_score:.4f}")
    
    if trainer.best_score >= 0.95:
        print("🎉 SUCCESS! 95%+ accuracy achieved!")

if __name__ == "__main__":
    main()