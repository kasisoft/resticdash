import fs from 'fs';
import path from 'path';
import yaml from 'yaml';

export async function load() {
    const i18nDir = './src/i18n';
    const files = fs.readdirSync(i18nDir);
    const dictionary = {};
    files.forEach(file => {
        const filename = path.basename(file);
        if (filename.endsWith('.yaml')) {
            const language = filename.substring(0, filename.length - '.yaml'.length);
            const fileContent = fs.readFileSync(i18nDir + '/' +file, 'utf8');
            const parsed = yaml.parse(fileContent);
            dictionary[language] = parsed;
        }
    });
    return {
        "dictionary": dictionary
    }
}
