package ca.sheridancollege.jaramisi.controllers;

import java.time.LocalDate;

import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import ca.sheridancollege.jaramisi.beans.Student;

@Controller
public class HomeController {

	@GetMapping("/")
	public String index(Model model) {
		return "index";
	}

	@PostMapping("/formPost")
	public String formPost(Model model,
			@RequestParam("firstName") String firstName, 
			@RequestParam("lastName") String lastName,
			@RequestParam("email") String email,
			@RequestParam("studentNumber") Long studentNumber,
			@RequestParam("birthday") @DateTimeFormat(iso=DateTimeFormat.ISO.DATE) LocalDate birthday) {
		
		Student student = new Student();
		student.setFirstName(firstName);
		student.setLastName(lastName);
		student.setEmail(email);
		student.setStudentNumber(studentNumber);
		student.setBirthday(birthday);
		
		System.out.println(student);
		
		return "working";
		
	}

}
