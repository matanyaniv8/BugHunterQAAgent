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
        <form id="test-form">
        <label for="credit-card">Credit Card:</label>
        <input type="text" id="credit-card" name="credit card"><br><br>
        <label for="phone-number">Phone Number:</label>
        <input type="text" id="phone-number" name="phone number"><br><br>
        <label for="birthdate">Birthdate:</label>
        <input type="text" id="birthdate" name="birthdate"><br><br>
        <label for="telephone">Telephone:</label>
        <input type="text" id="telephone" name="telephone"><br><br>
        <label for="confirm-password">Confirm Password:</label>
        <input type="text" id="confirm-password" name="confirm_password"><br><br>
        <input type="email" name="mail" >
        <input type="text" name="text" disabled>
        <input type="password" name="password" disabled>
        <input type="email" name="mail" disabled>
        <input type="text" name="phone number">
        <input type="number" name="number" disabled>
        <textarea name="textarea" disabled></textarea>
        <input type="checkbox" name="checkbox" disabled>
        <input type="radio" name="radio" disabled>
        <select name="select" disabled>
            <option value="">Select an option</option>
            <option value="1">Option 1</option>
        </select>
        <input type="submit" value="Submit" disabled>
        </form>
        '''
    ],
    "combined": [
        '''
        <form id="test-form">
        <input type="text" name="text" disabled>
        <label for="credit-card">Credit Card:</label>
        <input type="text" id="credit-card" name="credit card"><br><br>
        <label for="phone-number">Phone Number:</label>
        <input type="text" id="phone-number" name="phone number"><br><br>
        <label for="birthdate">Birthdate:</label>
        <input type="text" id="birthdate" name="birthdate"><br><br>
        <label for="telephone">Telephone:</label>
        <input type="text" id="telephone" name="telephone"><br><br>
        <label for="confirm-password">Confirm Password:</label>
        <input type="text" id="confirm-password" name="confirm_password"><br><br>
        <input type="password" name="password" disabled>
        <input type="email" name="email" disabled>
        <input type="number" name="number" disabled>
        <textarea name="textarea" disabled></textarea>
        <input type="checkbox" name="checkbox" disabled>
        <input type="radio" name="radio" disabled>
        <select name="select" disabled>
            <option value="">Select an option</option>
            <option value="1">Option 1</option>
        </select>
        <input type="submit" value="Submit" disabled>
        </form>
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
