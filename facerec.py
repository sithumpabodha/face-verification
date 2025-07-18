from deepface import DeepFace
import cv2
import os
import numpy as np

class FaceVerificationSystem:
    def __init__(self):
        self.models = ["Facenet", "ArcFace", "VGG-Face"]
        self.thresholds = {
            "Facenet": 0.70,
            "ArcFace": 0.68, 
            "VGG-Face": 0.60
        }
    
    def quality_check(self, img_path):
        """Professional quality assessment"""
        try:
            img = cv2.imread(img_path)
            if img is None: return 0.0
            h, w = img.shape[:2]
            
            # Resolution score (ideal 500px+)
            res_score = min(h, w) / 500
            
            # Sharpness score
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            sharp_score = min(sharpness / 100, 1.0)
            
            # Lighting score
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, _, _ = cv2.split(lab)
            light_score = min(cv2.mean(l)[0] / 127, 1.0)
            
            return min((res_score*0.4 + sharp_score*0.4 + light_score*0.2), 1.0)
        except:
            return 0.0
    
    def verify_faces(self, img1_path, img2_path):
        """Enterprise-grade verification"""
        try:
            # Quality assessment
            q1 = self.quality_check(img1_path)
            q2 = self.quality_check(img2_path)
            print(f"\nImage Quality Scores: {q1:.2f} | {q2:.2f} (1.0=perfect)")
            print()
            
            if q1 < 0.5 or q2 < 0.5:
                print("Warning: Low quality images may affect accuracy")
            
            # Multi-model verification
            results = []
            for model in self.models:
                result = DeepFace.verify(
                    img1_path=img1_path,
                    img2_path=img2_path,
                    model_name=model,
                    detector_backend="retinaface",
                    distance_metric="cosine",
                    threshold=self.thresholds[model],
                    align=True,
                    silent=True
                )
                results.append({
                    'model': model,
                    'verified': result['verified'],
                    'confidence': (1-result['distance'])*100,
                    'threshold': self.thresholds[model]*100
                })
            
            # Generate report
            self.generate_report(results, img1_path, img2_path)
            
        except Exception as e:
            print(f"System error: {str(e)}")
    
    def generate_report(self, results, img1_path, img2_path):
        """Professional reporting"""
        print("\n=== VERIFICATION REPORT ===")
        for res in results:
            status = "✅ MATCH" if res['verified'] else "❌ NO MATCH"
            print(f"{res['model']}: {status}")
            print(f"  Confidence: {res['confidence']:.2f}% (Threshold: {res['threshold']:.0f}%)")
        
        # Final verdict
        if all(r['verified'] for r in results):
            avg_conf = sum(r['confidence'] for r in results) / len(results)
            if avg_conf > 75:
                print("\nVERDICT: ✅✅ STRONG MATCH (High Confidence)")
            else:
                print("\nVERDICT: ✅ MATCH (Confirmed)")
        else:
            print("\nVERDICT: ❌ NO MATCH")
        
        # Face analysis
        print("\n=== FACE ANALYSIS ===")
        for i, path in enumerate([img1_path, img2_path]):
            print(f"\nImage {i+1}:")
            try:
                analysis = DeepFace.analyze(
                    img_path=path,
                    actions=['age', 'gender', 'emotion'],
                    detector_backend="retinaface",
                    silent=True
                )[0]
                print(f"• Age: {analysis.get('age', 'N/A')}")
                print(f"• Gender: {analysis.get('dominant_gender', 'N/A')}")
                print(f"• Emotion: {analysis.get('dominant_emotion', 'N/A')}")
            except:
                print("Analysis skipped (face not detected)")

if __name__ == "__main__":
    print("=== PROFESSIONAL FACE VERIFICATION SYSTEM ===")
    verifier = FaceVerificationSystem()
    
    img1 = input("First image path: ").strip('"')
    img2 = input("Second image path: ").strip('"')
    
    if not all(os.path.exists(p) for p in [img1, img2]):
        print("Error: One or both images not found")
    else:
        verifier.verify_faces(img1, img2)
    
    input("\nPress Enter to exit...")