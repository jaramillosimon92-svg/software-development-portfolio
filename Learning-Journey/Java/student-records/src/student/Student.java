package student;

/** Stores the information for one student. */
public class Student {
    private int id;
    private String lastName;
    private double finalGrade;

    public Student(int id, String lastName, double finalGrade) {
        this.id = id;
        this.lastName = lastName;
        this.finalGrade = finalGrade;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public double getFinalGrade() {
        return finalGrade;
    }

    public void setFinalGrade(double finalGrade) {
        this.finalGrade = finalGrade;
    }

    @Override
    public String toString() {
        return "ID: " + id + ", Last name: " + lastName
                + ", Final grade: " + finalGrade;
    }
}
