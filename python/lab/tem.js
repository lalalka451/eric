// Function to click an element by XPath
function clickElementByXPath(xpath) {
    const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (element) {
        element.click();
        return true;
    }
    return false;
}

// Function to set input value by XPath
function setInputValueByXPath(xpath, value) {
    const input = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (input) {
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        return true;
    }
    return false;
}

// Function to set select value by XPath
function setSelectValueByXPath(xpath, value) {
    const select = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (select) {
        select.value = value;
        select.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
    }
    return false;
}

// Function to generate a random name
function generateRandomName() {
    const names = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Quinn", "Avery", "Charlie"];
    return names[Math.floor(Math.random() * names.length)] + Math.floor(Math.random() * 1000);
}

// Main function to automate the signup process
function automateSignup() {
    const signupButtonXPath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/button/span/span';
    const createAccountButtonXPath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div/span/span';
    const nameInputXPath = '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/label/div/div[2]/div/input';
    const useEmailButtonXPath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/button/span';
    const emailInputXPath = '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/label/div/div[2]/div/input';
    const dateSelectorsXPath = '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[3]/div/div/select';
    const nextButtonXPath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span';

    // Click signup button
    if (clickElementByXPath(signupButtonXPath)) {
        console.log('Signup button clicked successfully');
        
        // Wait and click create account button
        setTimeout(() => {
            if (clickElementByXPath(createAccountButtonXPath)) {
                console.log('Create account button clicked successfully');
                
                // Wait and fill in email, birth date, and finally name
                setTimeout(() => {
                    if (clickElementByXPath(useEmailButtonXPath)) {
                        console.log('Use email instead button clicked successfully');
                    }
                    
                    setTimeout(() => {
                        if (setInputValueByXPathWithEvents(emailInputXPath, 'novelof391@scarden.com')) {
                            console.log('Email entered successfully');
                        } else {
                            console.log('Email input not found');
                        }

                        const dateSelectors = document.evaluate(dateSelectorsXPath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

                        if (dateSelectors.snapshotLength === 3) {
                            dateSelectors.snapshotItem(0).value = '1';
                            dateSelectors.snapshotItem(0).dispatchEvent(new Event('change', { bubbles: true }));
                            console.log('Month set to 01 successfully');

                            dateSelectors.snapshotItem(1).value = '1';
                            dateSelectors.snapshotItem(1).dispatchEvent(new Event('change', { bubbles: true }));
                            console.log('Day set to 01 successfully');

                            dateSelectors.snapshotItem(2).value = '2000';
                            dateSelectors.snapshotItem(2).dispatchEvent(new Event('change', { bubbles: true }));
                            console.log('Year set to 2000 successfully');

                            // Input name last
                            setTimeout(() => {
                                const randomName = generateRandomName();
                                if (setInputValueByXPathWithEvents(nameInputXPath, randomName)) {
                                    console.log('Random name entered successfully:', randomName);

                                    // Wait 1 second and input the name again
                                    setTimeout(() => {
                                        if (setInputValueByXPathWithEvents(nameInputXPath, randomName)) {
                                            console.log('Random name re-entered after 1 second');

                                            // Click the Next button after all inputs are filled
                                            setTimeout(() => {
                                                if (clickElementByXPath(nextButtonXPath)) {
                                                    console.log('Next button clicked successfully');
                                                } else {
                                                    console.log('Next button not found');
                                                }
                                            }, 1000); // Wait 1 second before clicking Next
                                        } else {
                                            console.log('Failed to re-enter name');
                                        }
                                    }, 1000);
                                } else {
                                    console.log('Name input not found or failed to enter');
                                }
                            }, 1000); // Wait 1 second before inputting name
                        } else {
                            console.log('Date selectors not found or incorrect number of selectors');
                        }
                    }, 1000); // Wait 1 second for email input to appear
                }, 2000);
            } else {
                console.log('Create account button not found');
            }
        }, 2000);
    } else {
        console.log('Signup button not found');
    }
}

// Function to set input value by XPath with additional events
function setInputValueByXPathWithEvents(xpath, value) {
    const input = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (input) {
        // Set the value attribute
        input.setAttribute('value', value);
        
        // Set the value property
        input.value = value;
        
        // Trigger events
        input.focus();
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true, cancelable: true, key: 'Enter', keyCode: 13 }));
        input.dispatchEvent(new KeyboardEvent('keypress', { bubbles: true, cancelable: true, key: 'Enter', keyCode: 13 }));
        input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true, cancelable: true, key: 'Enter', keyCode: 13 }));
        
        // Force a re-render if needed (this might help with React-based forms)
        setTimeout(() => {
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }, 0);
        
        return true;
    }
    return false;
}

// Run the automation after a short delay
setTimeout(automateSignup, 2000);
