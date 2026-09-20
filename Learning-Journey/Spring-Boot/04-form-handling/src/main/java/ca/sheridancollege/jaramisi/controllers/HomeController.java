package ca.sheridancollege.jaramisi.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {
	
	@GetMapping("/")
	public String index(Model model) {
		return "index";
	}
	
	@GetMapping("/hairColour")
	public String hairColour(Model model) {
	return "hairColour";
	}
	
	@GetMapping("/perfectHeight")
	public String perfectHeight(Model model) {
	return "perfectHeight";
	}
	
	@GetMapping("/preferredName")
	public String preferredName(Model model) {
	return "preferredName";
	}
}
