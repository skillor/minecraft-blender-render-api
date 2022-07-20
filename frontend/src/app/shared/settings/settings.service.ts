import { Injectable } from '@angular/core';
import { Setting } from './setting';

@Injectable({
    providedIn: 'root'
})
export class SettingsService {

    private localStoragePrefix = 'settings_';
    private settings: { [key: string]: Setting };

    constructor(
    ) {
        // default settings
        const settings: Setting[] = [
            {
                key: 'minecraft_blender_render_api_url',
                type: 'text',
                title: 'Minecraft Blender Render Api Url',
                value: 'https://minecraf-blender-render-api.herokuapp.com/',
            },
            {
                key: 'minecraft_blender_render_api_key',
                type: 'text',
                title: 'Minecraft Blender Render Api Key',
                value: '',
            },
        ];
        this.settings = {};
        for (const setting of settings) {
            this.settings[setting.key] = setting;
        }
        this.loadSettings();
    }

    private getLocalStorageKey(key: string): string {
        return this.localStoragePrefix + key;
    }

    private loadSetting(setting: Setting): void {
        const storedSetting = localStorage.getItem(this.getLocalStorageKey(setting.key));
        if (storedSetting === null) return;
        setting.value = JSON.parse(storedSetting);
    }

    private loadSettings(): void {
        for (const setting of Object.values(this.settings)) {
            this.loadSetting(setting);
        }
    }

    getSetting(key: string): Setting {
        return this.settings[key];
    }

    getSettings(): Setting[] {
        return Object.values(this.settings);
    }

    setSetting(key: string, value: any): void {
        if (this.settings[key].value === undefined || this.settings[key].value !== value) {
            this.settings[key].value = value;
            this.settings[key].change_callback?.(value);
        }
    }

    saveSettings(): void {
        for (const setting of Object.values(this.settings)) {
            this.saveSetting(setting);
        }
    }

    private saveSetting(setting: Setting): void {
        if (setting.value === undefined) return;
        localStorage.setItem(this.getLocalStorageKey(setting.key), JSON.stringify(setting.value));
    }
}
