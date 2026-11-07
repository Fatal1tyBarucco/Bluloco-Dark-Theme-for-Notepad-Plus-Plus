# Sample Java code to test Bluloco Dark
import java.util.*;
import java.util.stream.*;

/**
 * Tests Java 17+ features: Records, Streams, and Lambdas
 */
public record User(String name, int id) {}

public class Main {
    public static void main(String[] args) {
        List<User> users = List.of(new User("Alice", 1), new User("Bob", 2));
        
        users.stream()
             .filter(u -> u.id() > 0)
             .forEach(u -> System.out.println("User: " + u.name()));
    }
}
