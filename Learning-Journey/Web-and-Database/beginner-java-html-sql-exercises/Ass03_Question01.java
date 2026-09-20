/**
 * PROG23863 - Object Oriented Programming (Java)
 * Assignment 3 - Question 1
 * 
 * This file contains the Employee class (as per the UML diagram)
 * and a testing class (Ass03_Question01) that creates two Employee objects.
 *
 * Employee UML Fields:
 *   - name       : String
 *   - id         : int
 *   - department : String
 *   - position   : String
 *
 * Employee UML Methods:
 *   + Employee()
 *   + Employee(name, id, department, position)
 *   + getName()       : String
 *   + setName()       : void
 *   + getId()         : int
 *   + setId()         : void
 *   + getDepartment() : String
 *   + setDepartment() : void
 *   + getPosition()   : String
 *   + setPosition()   : void
 */

// ─────────────────────────────────────────────
// Employee class (non-public so it can share
// this file with the main/testing class)
// ─────────────────────────────────────────────
class Employee {

    // ── Private instance variables (from UML) ──
    private String name;
    private int    id;
    private String department;
    private String position;

    // ── Default (no-arg) constructor ──
    public Employee() {
        name       = "Unknown";
        id         = 0;
        department = "Unknown";
        position   = "Unknown";
    }

    // ── Parameterized constructor ──
    public Employee(String name, int id, String department, String position) {
        this.name       = name;
        this.id         = id;
        this.department = department;
        this.position   = position;
    }

    // ── Accessor (getter) for name ──
    public String getName() {
        return name;
    }

    // ── Mutator (setter) for name ──
    public void setName(String name) {
        this.name = name;
    }

    // ── Accessor (getter) for id ──
    public int getId() {
        return id;
    }

    // ── Mutator (setter) for id ──
    public void setId(int id) {
        this.id = id;
    }

    // ── Accessor (getter) for department ──
    public String getDepartment() {
        return department;
    }

    // ── Mutator (setter) for department ──
    public void setDepartment(String department) {
        this.department = department;
    }

    // ── Accessor (getter) for position ──
    public String getPosition() {
        return position;
    }

    // ── Mutator (setter) for position ──
    public void setPosition(String position) {
        this.position = position;
    }

    // ── toString: returns a readable description of the Employee ──
    @Override
    public String toString() {
        return "-----------------------------\n"
             + "Employee Name  : " + name       + "\n"
             + "Employee ID    : " + id         + "\n"
             + "Department     : " + department + "\n"
             + "Position       : " + position   + "\n"
             + "-----------------------------";
    }

} // end class Employee


// ─────────────────────────────────────────────
// Testing / Main class
// ─────────────────────────────────────────────
public class Ass03_Question01 {

    public static void main(String[] args) {

        // ── Create Employee object 1 using parameterized constructor (my data) ──
        Employee emp1 = new Employee("Alex Smith", 10234, "Computer Studies", "Software Developer");

        // ── Create Employee object 2 using default constructor, then set fields (friend's data) ──
        Employee emp2 = new Employee();
        emp2.setName("Jordan Lee");
        emp2.setId(10567);
        emp2.setDepartment("Information Technology");
        emp2.setPosition("Systems Analyst");

        // ── Display Employee 1 details ──
        System.out.println("Employee 1 Details:");
        System.out.println(emp1.toString());

        // ── Display Employee 2 details ──
        System.out.println("\nEmployee 2 Details:");
        System.out.println(emp2.toString());

        // ── Additional demonstration: using getters individually ──
        System.out.println("\nVerifying via individual getters:");
        System.out.println("Emp1 Name       : " + emp1.getName());
        System.out.println("Emp1 ID         : " + emp1.getId());
        System.out.println("Emp1 Department : " + emp1.getDepartment());
        System.out.println("Emp1 Position   : " + emp1.getPosition());

    } // end main

} // end class Ass03_Question01
