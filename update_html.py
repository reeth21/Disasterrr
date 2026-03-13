import sys
import re

file_path = "F:\Disaster\index.html"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    firebase_logic = """        // Initialize Firebase
        const firebaseConfig = {
            apiKey: "AIzaSyCUuj7P52-n2vOOeOhsDiHwW5R-uf8r25Y",
            authDomain: "disaster-5fe05.firebaseapp.com",
            projectId: "disaster-5fe05",
            storageBucket: "disaster-5fe05.firebasestorage.app",
            messagingSenderId: "212670668505",
            appId: "1:212670668505:web:27cba429eb12fa6a4e68c8",
            measurementId: "G-WQ7B5TQPQD",
            databaseURL: "https://disaster-5fe05-default-rtdb.firebaseio.com/"
        };
        firebase.initializeApp(firebaseConfig);
        const database = firebase.database();"""

    if "const database = firebase.database();" not in content:
        content = content.replace("const state =", f"{firebase_logic}\n\n        // Application State\n        const state =")

    sync_logic = """        function initializeFlats() {
            // Initialize local structure
            state.flats = [];
            for (let floor = 1; floor <= 8; floor++) {
                for (let flat = 1; flat <= 4; flat++) {
                    const flatNumber = floor * 100 + flat;
                    state.flats.push({
                        flatNumber: flatNumber,
                        floor: floor,
                        sensors: { gas: 20, smoke: 10, fire: 25, temperature: 20, water: 0, motion: 20 },
                        hasAlert: false, 
                        alertSensor: null
                    });
                }
            }
            
            // Sync to Firebase
            const flatsRef = database.ref('flats');
            flatsRef.on('value', (snapshot) => {
                const data = snapshot.val();
                if (data) {
                    state.flats.forEach(f => {
                        if(data[f.flatNumber]) {
                            f.sensors = data[f.flatNumber].sensors || f.sensors;
                            let alertFound = false;
                            Object.keys(f.sensors).forEach(sensorType => {
                                if(f.sensors[sensorType] > state.thresholds[sensorType]) {
                                    if(!f.hasAlert) triggerAlert(f.flatNumber, sensorType, false);
                                    alertFound = true;
                                }
                            });
                            if(!alertFound && f.hasAlert) {
                                f.hasAlert = false;
                                f.alertSensor = null;
                            }
                        }
                    });
                    if(state.isLoggedIn) render();
                } else {
                    const initialData = {};
                    state.flats.forEach(f => {
                        initialData[f.flatNumber] = { sensors: f.sensors };
                    });
                    flatsRef.set(initialData);
                }
            });
        }"""
        
    old_init = """        function initializeFlats() {
            state.flats = [];
            for (let floor = 1; floor <= 8; floor++) {
                for (let flat = 1; flat <= 4; flat++) {
                    const flatNumber = floor * 100 + flat;
                    state.flats.push({
                        flatNumber,
                        floor,
                        sensors: {
                            gas: 20,
                            smoke: 10,
                            fire: 25,
                            temperature: 20,
                            water: 0,
                            motion: 20
                        },
                        hasAlert: false,
                        alertSensor: null
                    });
                }
            }
        }"""
        
    content = content.replace(old_init, sync_logic)

    if 'function triggerAlert(flatNumber, sensorType) {' in content:
        content = content.replace('function triggerAlert(flatNumber, sensorType) {', 'function triggerAlert(flatNumber, sensorType, updateDb = true) {')
        
    if 'flat.sensors[sensorType] = state.thresholds[sensorType] * 1.3;' in content:
        content = content.replace('flat.sensors[sensorType] = state.thresholds[sensorType] * 1.3;', 'flat.sensors[sensorType] = state.thresholds[sensorType] * 1.3;\n            if (updateDb) {\n                database.ref("flats/" + flatNumber + "/sensors/" + sensorType).set(state.thresholds[sensorType] * 1.3);\n            }')

    # Add missing DB triggers to manual simulator
    old_sim = 'const val = parseFloat(this.value);\n                                                   /* Firebase push logic will go here */'
    new_sim = 'const val = parseFloat(this.value);\n                                                   database.ref("flats/" + state.selectedFlat + "/sensors/" + `${sensorType}`).set(val);'
    content = content.replace(old_sim, new_sim)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Firebase state integration successful")
except Exception as e:
    print(f"Error: {e}")
