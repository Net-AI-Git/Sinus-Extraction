# Sinus Extraction - Image Segmentation

מחברת Jupyter למימוש מודל Segmentation לזיהוי סינוסים בתמונות.

## שימוש ב-Google Colab

### טעינת המחברת ישירות מ-GitHub:

1. פתח [Google Colab](https://colab.research.google.com/)
2. לחץ על **File** → **Open notebook**
3. בחר בכרטיסייה **GitHub**
4. הדבק את כתובת ה-URL של המאגר:
   ```
   https://github.com/YOUR_USERNAME/Sinus_Extraction
   ```
5. בחר את המחברת: `Segmentation_code_templates/ImageSegmentation_template.ipynb`
6. לחץ על **Open**

### או השתמש בקישור ישיר:

לאחר העלאת המחברת ל-GitHub, תוכל להשתמש בקישור ישיר:
```
https://colab.research.google.com/github/YOUR_USERNAME/Sinus_Extraction/blob/main/Segmentation_code_templates/ImageSegmentation_template.ipynb
```

## עדכון המחברת

כאשר תעשה שינויים במחברת ותעלה אותם ל-GitHub:

1. ב-Colab, לחץ על **File** → **Revert to last saved version** (אם יש שינויים לא שמורים)
2. או רענן את הדף (F5) כדי לטעון את הגרסה החדשה מ-GitHub

## דרישות

המחברת כוללת את כל הפקודות להתקנת החבילות הנדרשות. פשוט הרץ את התאים בסדר.

## מבנה הפרויקט

```
Sinus_Extraction/
└── Segmentation_code_templates/
    └── ImageSegmentation_template.ipynb
```

## הערות

- המחברת מוכנה לשימוש ב-Colab עם GPU
- כל הנתיבים מותאמים לסביבת Colab (`/content/`)
- המחברת כוללת תצורת UNet עם ResNet18 backbone

