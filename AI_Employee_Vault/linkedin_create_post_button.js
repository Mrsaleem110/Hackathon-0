// ==UserScript==
// @name         LinkedIn Agentic Sphere - Create Post Button
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Add a quick "Create Post" button to Agentic Sphere page
// @author       Agentic Sphere
// @match        https://www.linkedin.com/company/agentic-sphere/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Wait for page to load
    function addCreatePostButton() {
        // Find the page header area
        const pageHeader = document.querySelector('[data-test-id="page-header"]') ||
                          document.querySelector('header') ||
                          document.querySelector('[class*="header"]');

        if (!pageHeader) {
            setTimeout(addCreatePostButton, 1000);
            return;
        }

        // Check if button already exists
        if (document.getElementById('agentic-create-post-btn')) {
            return;
        }

        // Create button container
        const buttonContainer = document.createElement('div');
        buttonContainer.style.cssText = `
            display: inline-block;
            margin: 10px;
            padding: 8px 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 24px;
            cursor: pointer;
            font-weight: 600;
            color: white;
            font-size: 14px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            z-index: 1000;
        `;

        const button = document.createElement('button');
        button.id = 'agentic-create-post-btn';
        button.textContent = '✨ Create Post';
        button.style.cssText = `
            background: none;
            border: none;
            color: white;
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
            padding: 0;
            margin: 0;
        `;

        button.addEventListener('mouseover', () => {
            buttonContainer.style.transform = 'translateY(-2px)';
            buttonContainer.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
        });

        button.addEventListener('mouseout', () => {
            buttonContainer.style.transform = 'translateY(0)';
            buttonContainer.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
        });

        button.addEventListener('click', () => {
            // Find and click the actual "Create a post" button on the page
            const createPostButtons = document.querySelectorAll('button');
            let found = false;

            for (let btn of createPostButtons) {
                if (btn.textContent.includes('Create a post') ||
                    btn.getAttribute('aria-label')?.includes('Create a post')) {
                    btn.click();
                    found = true;
                    break;
                }
            }

            if (!found) {
                alert('Could not find the Create a post button. Please try clicking it manually.');
            }
        });

        buttonContainer.appendChild(button);

        // Insert button near the top of the page
        const targetArea = document.querySelector('[class*="page-header"]') ||
                          document.querySelector('main') ||
                          document.body;

        if (targetArea) {
            targetArea.insertBefore(buttonContainer, targetArea.firstChild);
        }
    }

    // Run when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addCreatePostButton);
    } else {
        addCreatePostButton();
    }

    // Also run periodically in case page updates
    setInterval(addCreatePostButton, 5000);
})();
