import { Location } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { SettingsService } from '../settings/settings.service';
import { Observable, scan } from 'rxjs';
import { calculateState, initialState, Transfer } from './transfer';

@Injectable({
    providedIn: 'root'
})
export class MinecraftBlenderRenderService {

    constructor(
        private http: HttpClient,
        private settingsService: SettingsService,
    ) { }

    private getUrl(endpoint: string, args: { [key: string]: string } = {}): string {
        const url = new URL(
            Location.joinWithSlash(this.settingsService.getSetting('minecraft_blender_render_api_url').value, endpoint)
        );
        return url.toString();
    }

    renderSkinAuto(
        sceneFile: File,
        replaceAlexSkins: string | undefined = undefined,
        replaceSteveSkins: string | undefined = undefined,
        renderSettings: string | undefined = undefined,
    ): Observable<Transfer> {
        const formData = new FormData();
        formData.append('scene_file', sceneFile);
        if (replaceAlexSkins !== undefined && replaceAlexSkins !== '') formData.append('replace_skins_alex', replaceAlexSkins);
        if (replaceSteveSkins !== undefined && replaceSteveSkins !== '') formData.append('replace_skins_steve', replaceSteveSkins);
        if (renderSettings !== undefined && renderSettings !== '') formData.append('render_settings', renderSettings);
        return this.http.post(this.getUrl('/render-skin-auto'), formData, {
            reportProgress: true,
            observe: 'events',
            responseType: 'blob',
        }).pipe(
            scan(calculateState, initialState),
        );
    }
}