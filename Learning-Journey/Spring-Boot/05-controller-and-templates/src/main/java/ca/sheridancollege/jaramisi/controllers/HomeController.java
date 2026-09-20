package ca.sheridancollege.jaramisi.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

		@GetMapping("/")
		public String index(Model model) {
			return "index"; // no need to type .html because we are using thymeleaf
		}
		
		@GetMapping("/sayHi")
		public String sayHi(Model model) {
			return "sayHi";
		}
}
	
