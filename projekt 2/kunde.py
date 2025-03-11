import re

class Kunde:
   def __init__( self, id, name, adresse,email, vip_status=False):
         self.id = id
         self.name = name
         self.adresse = adresse
         self.email = email
         self.vip_status = vip_status

   def get_info(self):
       return f"Name: {self.name}, Adresse: {self.adresse}, E-Mail: {self.email}"

   def update_email(self, neue_email):
       self.email = neue_email
       print(f"Die E-Mail-Adresse von {self.name} wurde auf {self.email} geaendert.")

   def update_address(self, neue_adresse):
       self.adresse = neue_adresse
       print(f"Adresse für {self.name} wurde auf {self.adresse} aktualisiert.")

    
    #  update_email
   def update_email(self, neue_email):
 
       email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
       if re.match(email_pattern, neue_email):
           self.email = neue_email
           print(f"Die E-Mail von {self.name} wurde auf {self.email} aktualisiert.")
       else:
           print("Ungültige E-Mail-Adresse!")