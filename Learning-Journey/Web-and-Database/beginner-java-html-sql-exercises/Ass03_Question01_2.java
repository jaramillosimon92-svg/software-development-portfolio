// PROG23863 - Assignment 3 - Question 1
// This program creates an Employee class and tests it with 2 objects
// User enters data for both employees from the keyboard

import java.util.Scanner;

class Employee {

    // instance variables
    private String name;
    private int id;
    private String department;
    private String position;

    // default constructor
    public Employee() {
        name = "";
        id = 0;
        department = "";
        position = "";
    }

    // constructor with parameters
    public Employee(String name, int id, String department, String position) {
        this.name = name;
        this.id = id;
        this.department = department;
        this.position = position;
    }

    // getter for name
    public String getName() {
        return name;
    }

    // setter for name
    public void setName(String name) {
        this.name = name;
    }

    // getter for id
    public int getId() {
        return id;
    }

    // setter for id
    public void setId(int id) {
        this.id = id;
    }

    // getter for department
    public String getDepartment() {
        return department;
    }

    // setter for department
    public void setDepartment(String department) {
        this.department = department;
    }

    // getter for position
    public String getPosition() {
        return position;
    }

    // setter for position
    public void setPosition(String position) {
        this.position = position;
    }

    // toString method to display employee info
    public String toString() {
        return "Name: " + name + "\nID: " + id + "\nDepartment: " + department + "\nPosition: " + position;
    }

}

public class Ass03_Question01 {

    public static void main(String[] args) {

        Scanner input = new Scanner(System.in);

        // --- Employee 1 (my data) ---
        System.out.println("Enter details for Employee 1 (your info):");

        System.out.print("Enter name: ");
        String name1 = input.nextLine();
        // validate that name is not empty
        while (name1.trim().isEmpty()) {
            System.out.print("Name cannot be empty. Enter name: ");
            name1 = input.nextLine();
        }

        System.out.print("Enter ID (numbers only): ");
        // validate that id is a positive integer
        while (!input.hasNextInt()) {
            System.out.print("Invalid ID. Enter a number: ");
            input.next();
        }
        int id1 = input.nextInt();
        while (id1 <= 0) {
            System.out.print("ID must be a positive number. Enter ID: ");
            while (!input.hasNextInt()) {
                System.out.print("Invalid ID. Enter a number: ");
                input.next();
            }
            id1 = input.nextInt();
        }
        input.nextLine(); // clear the newline left in the buffer

        System.out.print("Enter department: ");
        String dept1 = input.nextLine();
        while (dept1.trim().isEmpty()) {
            System.out.print("Department cannot be empty. Enter department: ");
            dept1 = input.nextLine();
        }

        System.out.print("Enter position: ");
        String pos1 = input.nextLine();
        while (pos1.trim().isEmpty()) {
            System.out.print("Position cannot be empty. Enter position: ");
            pos1 = input.nextLine();
        }

        // create first employee using parameterized constructor
        Employee emp1 = new Employee(name1, id1, dept1, pos1);

        // --- Employee 2 (friend's data) ---
        System.out.println("\nEnter details for Employee 2 (your friend's info):");

        System.out.print("Enter name: ");
        String name2 = input.nextLine();
        while (name2.trim().isEmpty()) {
            System.out.print("Name cannot be empty. Enter name: ");
            name2 = input.nextLine();
        }

        System.out.print("Enter ID (numbers only): ");
        while (!input.hasNextInt()) {
            System.out.print("Invalid ID. Enter a number: ");
            input.next();
        }
        int id2 = input.nextInt();
        while (id2 <= 0) {
            System.out.print("ID must be a positive number. Enter ID: ");
            while (!input.hasNextInt()) {
                System.out.print("Invalid ID. Enter a number: ");
                input.next();
            }
            id2 = input.nextInt();
        }
        input.nextLine(); // clear the newline left in the buffer

        System.out.print("Enter department: ");
        String dept2 = input.nextLine();
        while (dept2.trim().isEmpty()) {
            System.out.print("Department cannot be empty. Enter department: ");
            dept2 = input.nextLine();
        }

        System.out.print("Enter position: ");
        String pos2 = input.nextLine();
        while (pos2.trim().isEmpty()) {
            System.out.print("Position cannot be empty. Enter position: ");
            pos2 = input.nextLine();
        }

        // create second employee using default constructor then setters
        Employee emp2 = new Employee();
        emp2.setName(name2);
        emp2.setId(id2);
        emp2.setDepartment(dept2);
        emp2.setPosition(pos2);

        // display both employees
        System.out.println("\nEmployee 1:");
        System.out.println(emp1.toString());

        System.out.println("\nEmployee 2:");
        System.out.println(emp2.toString());

        input.close();

    }

}
