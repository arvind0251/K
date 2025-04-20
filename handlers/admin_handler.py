from telegram import Update
from telegram.ext import CallbackContext
from database.models import add_country, add_service, add_promo
from config import ADMIN_ID

#admin 
@@ def admin_text(update: Update, context: CallbackContext):
-    if action == "add_country":
-        try:
-            name, cid = [x.strip() for x in text.split(",")]
-            add_country(name, int(cid))
-            update.message.reply_text(f"✅ Country Added:\nName: {name}\nID: {cid}")
-        except:
-            update.message.reply_text("❌ Format: India,22")
+    if action == "add_country":
+        try:
+            name, cid = [x.strip() for x in text.split(",")]
+            add_country(name, int(cid))
+            update.message.reply_text(
+                f"✅ Country Added:\nName: {name}\nID: {cid}"
+            )
+        except:
+            update.message.reply_text(
+                "❌ Format: Name,ID (e.g. India,22)"
+            )

    elif action == "add_service_to_country":
        try:
            # Service के लिए Name, ServiceID, Price
            name, sid, price = [x.strip() for x in text.split(",")]
            cid   = context.user_data.get("admin_country_id")
            cname = context.user_data.get("admin_country_name")

            add_service(name, sid, int(price), cid, cname)
            update.message.reply_text(f"✅ Service added to {cname}: {name} ₹{price}")
        except:
            update.message.reply_text("❌ Format: Name,ID,Price (e.g. Telegram,telegram,20)")

    elif action == "add_promo":
        try:
            code, amount = [x.strip() for x in text.split(",")]
            add_promo(code, int(amount))
            update.message.reply_text(f"✅ Promo added: {code} ₹{amount}")
        except:
            update.message.reply_text("❌ Format: CODE,amount (e.g. WELCOME100,10)")

    # काम होने के बाद action साफ़ कर दें
    context.user_data.pop("admin_action", None)
