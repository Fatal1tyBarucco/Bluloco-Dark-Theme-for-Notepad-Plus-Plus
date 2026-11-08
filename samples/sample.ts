// Sample TypeScript code to test Bluloco Dark
interface User {
    id: number;
    username: string;
    email?: string;
}

type Role = 'Admin' | 'User' | 'Guest';

class UserManager<T extends User> {
    private users: T[] = [];

    addUser(user: T): void {
        this.users.push(user);
    }

    findUser(id: number): T | undefined {
        return this.users.find(u => u.id === id);
    }
}

const manager = new UserManager<User>();
