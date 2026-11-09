import sys
import unicodedata

subjects = {
    "1": "Python",
    "2": "คณิตศาสตร์",
    "3": "ฟิสิกส์"
}

students = []
next_student_number = 1
PASS_SCORE = 50
NO_DATA = "ยังไม่มีข้อมูล"


# ---------- ฟังก์ชันตัดสินผลและเกรด ----------

def check_pass(score):
    if score >= PASS_SCORE:
        return "ผ่าน"
    else:
        return "ไม่ผ่าน"


def calculate_grade(score):
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


# ---------- ฟังก์ชันคำนวณ ----------

def get_valid_scores(scores):
    return [score for score in scores if score is not None]


def calculate_total(scores):
    valid_scores = get_valid_scores(scores)
    if not valid_scores:
        return NO_DATA
    return sum(valid_scores)


def calculate_average(scores):
    valid_scores = get_valid_scores(scores)
    if not valid_scores:
        return NO_DATA
    return calculate_total(valid_scores) / len(valid_scores)


def find_max(scores):
    valid_scores = get_valid_scores(scores)
    if not valid_scores:
        return NO_DATA
    return max(valid_scores)


def find_min(scores):
    valid_scores = get_valid_scores(scores)
    if not valid_scores:
        return NO_DATA
    return min(valid_scores)


def format_value(value, spec="g"):
    """จัดรูปแบบตัวเลข ถ้าเป็นข้อความ (เช่น 'ยังไม่มีข้อมูล') จะคืนค่าเดิม"""
    if isinstance(value, str):
        return value
    return format(value, spec)


# ---------- ฟังก์ชันจัดการข้อมูลนักเรียน ----------

def generate_student_id():
    global next_student_number
    student_id = f"S{next_student_number:03d}"
    next_student_number += 1
    return student_id


def create_student(name):
    student = {"id": generate_student_id(), "name": name}
    for subject_name in subjects.values():
        student[subject_name] = None
    students.append(student)
    return student


def find_student(value, field="id"):
    """ค้นหานักเรียนจาก field ที่กำหนด ('id' หรือ 'name') ไม่พบคืน None"""
    for student in students:
        if student[field] == value:
            return student
    return None


def is_valid_name(name):
    """ชื่อต้องเป็นตัวอักษร (ไทย/อังกฤษ/ภาษาอื่น) และเว้นวรรคได้ ห้ามมีตัวเลขหรืออักขระพิเศษ"""
    if not name.replace(" ", ""):
        return False
    for char in name:
        if char == " ":
            continue
        
        if not (char.isalpha() or unicodedata.category(char).startswith("M")):
            return False
    return True


def get_student_scores(student):
    return [student[subject_name] for subject_name in subjects.values()]


# ---------- ฟังก์ชันรับข้อมูล / แสดงผลที่ใช้ร่วมกัน ----------

def read_int(message):
    """รับตัวเลขจำนวนเต็ม ถ้าไม่ใช่ตัวเลขจะแจ้งเตือนและคืน None"""
    try:
        return int(input(message))
    except ValueError:
        print("\nกรุณากรอกตัวเลขเท่านั้น")
        return None


def ask_yes_no(message):
    while True:
        answer = input(f"\n{message} (1=ใช่, 2=ไม่): ").strip()
        if answer == "1":
            return True
        if answer == "2":
            return False
        print("\nกรุณากรอก 1 หรือ 2 เท่านั้น")


def read_score(subject_name, name):
    """รับคะแนน 0-100 ถ้าใส่ -1 คืน None เพื่อกลับไปเลือกวิชา"""
    while True:
        try:
            score = float(input(
                f"คะแนน {subject_name} ของ {name} (ใส่ -1 เพื่อกลับไปเลือกวิชา): "
            ))
        except ValueError:
            print("\nกรุณากรอกคะแนนเป็นตัวเลข")
            continue

        if score == -1:
            return None
        if 0 <= score <= 100:
            return score
        print("\nคะแนนต้องอยู่ระหว่าง 0-100 เท่านั้น")


def choose_subject(title):
    """แสดงเมนูเลือกวิชา คืนชื่อวิชา หรือ None ถ้าเลือกกลับเมนูก่อนหน้า"""
    while True:
        print(f"\n--- {title} ---")
        for key, subject_name in subjects.items():
            print(f"{key}. {subject_name}")
        print("4. กลับเมนูก่อนหน้า")

        choice = read_int("กรุณาเลือกวิชา: ")
        if choice is None:
            continue

        match choice:
            case 1 | 2 | 3:
                return subjects[str(choice)]
            case 4:
                return None
            case _:
                print("กรุณาเลือกเมนู 1-4 เท่านั้น")


def print_student(student):
    print(f"\nID: {student['id']} | ชื่อ: {student['name']}")
    for subject_name in subjects.values():
        score = student[subject_name]
        if score is None:
            print(f"  {subject_name}: ยังไม่ได้กรอกคะแนน")
        else:
            print(
                f"  {subject_name}: {score:g} | "
                f"{check_pass(score)} | เกรด {calculate_grade(score)}"
            )


def print_student_list():
    print("\n--- รายชื่อนักเรียน ---")
    for student in students:
        print(f"{student['id']} | {student['name']}")


# ---------- เมนูกรอกคะแนน ----------

def add_scores():
    
    while True:
        
        subject_name = choose_subject("กรอกคะแนนนักเรียน")
        if subject_name is None:
            return

        print(f"\n--- กรอกคะแนนวิชา {subject_name} ---")
        print("กรอกชื่อและคะแนนทีละคน")
        student_count = 1
        while True:      
             
            name = " ".join(input(f"\nชื่อนักเรียนคนที่ {student_count} (ใส่ -1 เพื่อกลับไปเลือกวิชา): ").split())
            if name == "-1":
                print("กลับไปเลือกวิชา")
                break

            if not is_valid_name(name):
                print("\nชื่อไม่ถูกต้อง! กรุณาใช้ตัวอักษรเท่านั้น")
                continue

            score = read_score(subject_name, name)
            if score is None:
                print("\nกลับไปเลือกวิชา")
                break

            student = find_student(name, "name")

            if student is None:
                student = create_student(name)
                print(f"เพิ่มนักเรียนใหม่สำเร็จ (ID: {student['id']})")
            elif student[subject_name] is not None:
                print(f"คะแนนเดิมของ {name} คือ {student[subject_name]:g}")
                if not ask_yes_no("ต้องการเปลี่ยนคะแนนหรือไม่"):
                    print("\nคงคะแนนเดิมไว้")
                    continue

            student[subject_name] = score
            student_count += 1
            print(f"บันทึกคะแนน {name} สำเร็จ\n")
            print(f"คะแนน: {score:g}")
            print(f"เกรด: {calculate_grade(score)}")
            print(f"ผลสอบ: {check_pass(score)}")


# ---------- เมนูแสดงคะแนน ----------

def show_subject_summary(subject_name):
    scored_students = [s for s in students if s[subject_name] is not None]

    if not scored_students:
        print(f"\nวิชา {subject_name} ยังไม่มีข้อมูลคะแนน")
        return

    scores = [s[subject_name] for s in scored_students]

    print(f"\n========== ผลคะแนนวิชา {subject_name} ==========")
    for student in scored_students:
        score = student[subject_name]
        print(
            f"{student['id']} | {student['name']} | คะแนน {score:g} | "
            f"{check_pass(score)} | เกรด {calculate_grade(score)}"
        )

    passed = sum(1 for score in scores if check_pass(score) == "ผ่าน")
    highest = find_max(scores)
    lowest = find_min(scores)

    print("\n--- สรุปสถิติ ---")
    print(f"จำนวนนักเรียน: {len(scores)} คน")
    print(f"ผ่าน: {passed} คน | ไม่ผ่าน: {len(scores) - passed} คน")
    print(f"คะแนนรวม: {format_value(calculate_total(scores))}")
    print(f"คะแนนเฉลี่ย: {format_value(calculate_average(scores), '.2f')}")
    print(f"คะแนนสูงสุด: {format_value(highest)}")
    for student in scored_students:
        if student[subject_name] == highest:
            print(f"  - {student['id']} | {student['name']}")
    print(f"คะแนนต่ำสุด: {format_value(lowest)}")
    for student in scored_students:
        if student[subject_name] == lowest:
            print(f"  - {student['id']} | {student['name']}")


def view_students():
    if not students:
        print("\nไม่มีข้อมูลนักเรียน")
        return

    for student in students:
        print_student(student)
        average = calculate_average(get_student_scores(student))
        print(f"  คะแนนเฉลี่ย: {format_value(average, '.2f')}")


def delete_student_data():
    while True:
        if not students:
            print("ไม่มีข้อมูลนักเรียน")
            return

        print("\n--- จัดการข้อมูลนักเรียน ---")
        print("1. แก้ไขคะแนนรายวิชา")
        print("2. ลบข้อมูลนักเรียนทุกวิชา")
        print("3. กลับเมนูก่อนหน้า")

        choice = read_int("กรุณาเลือกรายการ: ")
        if choice is None:
            continue

        if choice == 3:
            return

        if choice not in (1, 2):
            print("กรุณาเลือกเมนู 1-3 เท่านั้น")
            continue

        # แสดงรายชื่อและรหัสก่อนถามรหัสนักเรียน
        print_student_list()
        student_id = input("กรุณาใส่ ID นักเรียน: ").strip().upper()
        student = find_student(student_id)

        if student is None:
            print("ไม่พบข้อมูลนักเรียน")
            continue

        print_student(student)

        if choice == 1:
            subject_name = choose_subject(
                f"เลือกวิชาที่ต้องการแก้ไขคะแนนของ {student['name']}"
            )

            if subject_name is None:
                continue

            if student[subject_name] is None:
                print(f"นักเรียนคนนี้ยังไม่มีคะแนน {subject_name}")
                continue

            print(f"\nคะแนนเดิม: {student[subject_name]:g}")

            if ask_yes_no(f"ต้องการแก้ไขคะแนน {subject_name} หรือไม่"):
                new_score = read_score(subject_name, student['name'])

                if new_score is None:
                    print("\nยกเลิกการแก้ไขคะแนน")
                    continue

                student[subject_name] = new_score

                print("\nแก้ไขคะแนนสำเร็จ")
                print(f"คะแนนใหม่: {new_score:g}")
                print(f"เกรดใหม่: {calculate_grade(new_score)}")
                print(f"ผลสอบ: {check_pass(new_score)}")
            else:
                print("\nยกเลิกการแก้ไขคะแนน")

        else:
            if ask_yes_no("ยืนยันลบข้อมูลนักเรียนทั้งหมดหรือไม่"):
                students.remove(student)
                print(f"ลบข้อมูลของ {student['name']} สำเร็จ")
            else:
                print("\nยกเลิกการลบข้อมูล")


def show_scores():
    while True:
        if not students:
            print("\nไม่มีข้อมูลนักเรียน")
            return

        print("\n--- แสดงคะแนนนักเรียน ---")
        print("1. Python")
        print("2. คณิตศาสตร์")
        print("3. ฟิสิกส์")
        print("4. แสดงคะแนนทุกวิชา")
        print("5. กลับเมนูหลัก")

        choice = read_int("กรุณาเลือกเมนู: ")
        if choice is None:
            continue

        match choice:
            case 1 | 2 | 3:
                show_subject_summary(subjects[str(choice)])
            case 4:
                view_students()
            case 5:
                return
            case _:
                print("กรุณาเลือกเมนู 1-5 เท่านั้น")


# ---------- โปรแกรมหลัก ----------

def main():
    while True:
        print("\n========== Student Score Dashboard ==========")
        print("1. กรอกคะแนนนักเรียน")
        print("2. แสดงคะแนนนักเรียน")
        print("3. จัดการข้อมูลนักเรียน")
        print("4. ออกจากระบบ")

        choice = read_int("กรุณาเลือกเมนู: ")
        if choice is None:
            continue

        match choice:
            case 1:
                add_scores()
            case 2:
                show_scores()
            case 3:
                delete_student_data()
            case 4:
                if ask_yes_no("ยืนยันออกจากระบบหรือไม่"):
                    print("\nออกจากระบบเรียบร้อย")
                    sys.exit()
            case _:
                print("\nกรุณาเลือกเมนู 1-4 เท่านั้น")


if __name__ == "__main__":
    main()
