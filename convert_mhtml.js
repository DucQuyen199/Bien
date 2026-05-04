#!/usr/bin/env node
/**
 * MHTML to HTML Converter using mhtml-to-html library
 */

import { convert } from 'mhtml-to-html';
import { writeFileSync, mkdirSync, readFileSync, existsSync } from 'fs';
import { join, dirname, basename, extname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

async function convertMhtmlToHtml(inputFile, outputFile = null) {
    console.log('='.repeat(60));
    console.log('MHTML to HTML Converter (using mhtml-to-html library)');
    console.log('='.repeat(60));
    
    if (!existsSync(inputFile)) {
        console.error(`Error: File not found: ${inputFile}`);
        process.exit(1);
    }
    
    // Determine output file path
    if (!outputFile) {
        const dir = dirname(inputFile);
        const name = basename(inputFile, extname(inputFile));
        outputFile = join(dir, `${name}.html`);
    }
    
    console.log(`Input: ${inputFile}`);
    console.log(`Output: ${outputFile}`);
    console.log('');
    
    try {
        // Read the MHTML file
        const mhtmlContent = readFileSync(inputFile);
        
        // Convert using the library
        console.log('Converting...');
        const result = await convert(mhtmlContent);
        
        // Ensure output directory exists
        const outputDir = dirname(outputFile);
        mkdirSync(outputDir, { recursive: true });
        
        // Write the result
        writeFileSync(outputFile, result.data);
        
        console.log('');
        console.log('='.repeat(60));
        console.log('Conversion complete!');
        console.log(`Output file: ${outputFile}`);
        console.log(`File size: ${(result.length / 1024).toFixed(2)} KB`);
        console.log('='.repeat(60));
        
    } catch (error) {
        console.error('Error during conversion:', error.message);
        if (error.stack) {
            console.error(error.stack);
        }
        process.exit(1);
    }
}

// Also support CLI arguments for the library's built-in CLI
import { parseArgs } from 'util';

const args = process.argv.slice(2);

if (args.length === 0) {
    console.log('Usage:');
    console.log('  node convert_mhtml.js <input.mhtml> [output.html]');
    console.log('');
    console.log('Examples:');
    console.log('  node convert_mhtml.js article.mhtml');
    console.log('  node convert_mhtml.js article.mhtml output.html');
    process.exit(0);
}

const inputFile = args[0];
const outputFile = args[1] || null;

convertMhtmlToHtml(inputFile, outputFile);
