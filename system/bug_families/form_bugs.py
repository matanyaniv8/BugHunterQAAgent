forms_bugs = {
    "Drop-Down list selection validation": [
        '''
    <form id="Buggy Form">
        <label>Choose a car:</label>
        <select id="cars" name="">
            <option value="volvo">Volvo</option>
            <option value="saab">Saab</option>
            <option value="fiat" disabled>Fiat</option>
            <option value="audi">Audi</option>
        </select>
    </form>
        '''
    ],
    "inputs buttons": [
        '''
        <form id="buggyForm">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name"><br><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email">
        <button type="button" onclick="checkEmail()">Check Email</button><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password"><br><br>

        <label for="confirm_password">Confirm Password:</label>
        <input type="password" id="confirm_password">
        <button type="button" onclick="checkPasswords()">Check Passwords</button><br><br>
        '''
    ],
    "combined": [
        '''
        <form id="buggyForm">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name"><br><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email">
        <button type="button" onclick="checkEmail()">Check Email</button><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password"><br><br>

        <label for="confirm_password">Confirm Password:</label>
        <input type="password" id="confirm_password">
        <button type="button" onclick="checkPasswords()">Check Passwords</button><br><br>

        <label for="dropdown">Choose an option:</label>
        <select id="dropdown" name="dropdown">
            <option value="">Please select</option>
            <option>Option1</option>
            <option value="option2">Option 2</option>
        </select>
        <button type="button" onclick="checkDropdown()">Check Dropdown</button><br><br>

        <label>Choose a car:</label>
        <select id="cars" name="">
            <option value="volvo">Volvo</option>
            <option value="saab">Saab</option>
            <option value="fiat" disabled>Fiat</option>
            <option value="audi">Audi</option>
        </select>
        <button type="button" onclick="checkCarSelection()">Check Car</button><br><br>

        <label for="subscribe">Subscribe to newsletter:</label>
        <input type="checkbox" id="subscribe" name="subscribe"><br><br>

        <input type="submit" value="Submit">
    </form>
        '''
    ]
}