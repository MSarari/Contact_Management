import json

class ContactManager:
    def __init__(self, filename):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, 'r') as file:
                contacts = json.load(file)
            return contacts
        except FileNotFoundError:
            return []

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self, contact_id=None, name=None, phone=None, email=None):
        if contact_id is None:
            contact_id = self.generate_unique_id()
        
        if self.is_id_unique(contact_id):
            if name is None:
                name = input("الاسم: ")
            if phone is None:
                phone = input("رقم الجوال: ")
            if email is None:
                email = input("البريد الإلكتروني: ")

            contact = {
                'id': contact_id,
                'name': name,
                'phone': phone,
                'email': email
            }
            self.contacts.append(contact)
            self.save_contacts()
            print("تمت إضافة جهة الاتصال بنجاح!")
        else:
            print("خطأ: هذا الرقم مكرر. يرجى استخدام رقم آخر.")

    def update_contact(self, contact_id, name, phone, email):
        for contact in self.contacts:
            if contact['id'] == contact_id:
                contact['name'] = name
                contact['phone'] = phone
                contact['email'] = email
                self.save_contacts()
                print("تم تحديث جهة الاتصال بنجاح!")
                return
        print("خطأ: لم يتم العثور على جهة الاتصال")

    def delete_contact(self, contact_id):
        self.contacts = [contact for contact in self.contacts if contact['id'] != contact_id]
        self.save_contacts()
        print("تم حذف جهة الاتصال بنجاح!")

    def display_contacts(self):
        for contact in self.contacts:
            print(f"الرقم: {contact['id']}")
            print(f"الاسم: {contact['name']}")
            print(f"رقم الجوال: {contact['phone']}")
            print(f"البريد الإلكتروني: {contact['email']}")
            print("-------------------------")

    def search_contact(self, keyword):
        results = []
        for contact in self.contacts:
            if (keyword.lower() in contact['name'].lower()) or (keyword in contact['phone']) or (keyword in contact['email']):
                results.append(contact)
        return results

    def is_id_unique(self, contact_id):
        return all(contact['id'] != contact_id for contact in self.contacts)

    def generate_unique_id(self):
        if not self.contacts:
            return 1
        else:
            max_id = max(contact['id'] for contact in self.contacts)
            return max_id + 1

if __name__ == "__main__":
    manager = ContactManager("contacts.json")

    while True:
        print("1. إضافة جهة اتصال")
        print("2. تعديل جهة اتصال")
        print("3. حذف جهة اتصال")
        print("4. عرض جهات الاتصال")
        print("5. البحث في جهات الاتصال")
        print("6. الخروج")

        choice = int(input("الرجاء اختيار عملية: "))

        if choice == 1:
            contact_id_input = input("إذا كنت ترغب في إدخال الـ ID يدويًا، اتركه فارغًا. إلا فأدخل الـ ID: ")
            if contact_id_input:
                contact_id = int(contact_id_input)
            else:
                contact_id = None
            manager.add_contact(contact_id)

        elif choice == 2:
            contact_id = int(input("الرقم: "))
            name = input("الاسم: ")
            phone = input("رقم الجوال: ")
            email = input("البريد الإلكتروني: ")
            manager.update_contact(contact_id, name, phone, email)

        elif choice == 3:
            contact_id = int(input("الرقم: "))
            manager.delete_contact(contact_id)

        elif choice == 4:
            manager.display_contacts()

        elif choice == 5:
            keyword = input("كلمة البحث: ")
            results = manager.search_contact(keyword)
            if results:
                print("نتائج البحث:")
                for result in results:
                    print(f"الرقم: {result['id']}")
                    print(f"الاسم: {result['name']}")
                    print(f"رقم الجوال: {result['phone']}")
                    print(f"البريد الإلكتروني: {result['email']}")
                    print("-------------------------")
            else:
                print("لم يتم العثور على نتائج")

        elif choice == 6:
            print("تم الخروج من البرنامج")
            break