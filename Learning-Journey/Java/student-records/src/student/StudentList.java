package student;

public class StudentList {

    public static void main(String[] args) {
        Student[] studentList = new Student[5];
        Student s1 = new Student(1001, "Smith", 82.5);
        studentList[0] = s1;
        studentList[1] = new Student(1002, "Garcia", 91.0);
        studentList[2] = new Student(1003, "Patel", 76.5);
        studentList[3] = new Student(1004, "Chen", 95.5);
        studentList[4] = new Student(1005, "Brown", 88.0);

        System.out.println("Student information:");
        for (int i = 0; i < studentList.length; i++) {
            System.out.println(studentList[i]);
        }

        Student topStudent = TopStudent(studentList);
        System.out.println("\nTop student: " + topStudent.getLastName()
                + " (" + topStudent.getFinalGrade() + ")");
        System.out.println("Class average: " + CalcAvg(studentList));
    }

    public static Student TopStudent(Student[] studentList) {
        Student highest = studentList[0];

        for (int i = 1; i < studentList.length; i++) {
            if (studentList[i].getFinalGrade() > highest.getFinalGrade()) {
                highest = studentList[i];
            }
        }
        return highest;
    }

    public static double CalcAvg(Student[] studentList) {
        double total = 0;

        for (int i = 0; i < studentList.length; i++) {
            total += studentList[i].getFinalGrade();
        }
        return total / studentList.length;
    }
}
