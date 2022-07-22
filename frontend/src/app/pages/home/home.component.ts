import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { MinecraftBlenderRenderService } from 'src/app/shared/minecraft-blender-render/minecraft-blender-render.service';
import { Transfer } from 'src/app/shared/minecraft-blender-render/transfer';
import { SettingsService } from 'src/app/shared/settings/settings.service';
import { StorageService } from 'src/app/shared/storage/storage.service';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

    sceneFileName = '';

    renderForm: FormGroup;

    transferState?: Transfer;

    renderImageSrc?: SafeUrl = undefined;
    loadedRenderSettings?: any = undefined;
    errorMessage: string = '';

    constructor(
        private minecraftBlenderRenderService: MinecraftBlenderRenderService,
        public settingsService: SettingsService,
        private storageService: StorageService,
        private formBuilder: FormBuilder,
        private sanitizer: DomSanitizer,
    ) {
        this.renderForm = this.formBuilder.group({
            renderFile: new FormControl('', [Validators.required]),
            renderFileSource: new FormControl(<any>undefined, [Validators.required]),
            replaceAlexSkins: new FormControl(this.storageService.load('mcrape_replaceAlexSkins', '')),
            replaceSteveSkins: new FormControl(this.storageService.load('mcrape_replaceSteveSkins', '')),
            renderSettings: new FormControl(this.storageService.load('mcrape_renderSettings', `{"settings": {
    "cycles.use_denoising": true,
    "render.engine": "CYCLES",
    "cycles.samples": 1
}}`)),
        });
    }

    ngOnInit(): void {
        this.renderForm.valueChanges.subscribe(() => {
            this.storageService.save('mcrape_replaceAlexSkins', this.renderForm.get('replaceAlexSkins')?.value);
            this.storageService.save('mcrape_replaceSteveSkins', this.renderForm.get('replaceSteveSkins')?.value);
            this.storageService.save('mcrape_renderSettings', this.renderForm.get('renderSettings')?.value);
        });
    }

    get f() {
        return this.renderForm.controls;
    }

    onSceneFileSelected(event: any) {
        const file: File = event.target.files[0];

        if (file) {

            this.sceneFileName = file.name;

            this.renderForm.patchValue({
                renderFileSource: file
            });
        } else {
            this.sceneFileName = '';
        }
    }

    renderScene() {
        this.errorMessage = '';
        this.minecraftBlenderRenderService.renderSkinAuto(
            this.renderForm.get('renderFileSource')!.value,
            this.renderForm.get('replaceAlexSkins')!.value,
            this.renderForm.get('replaceSteveSkins')!.value,
            this.renderForm.get('renderSettings')!.value,
        ).subscribe(
            (transfer) => {
                this.transferState = transfer;
                if (transfer.state == 'DONE') {
                    this.transferState = undefined;
                    this.renderImageSrc = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(transfer.event?.body));
                }
            },
            (error) => {
                this.errorMessage = 'Something went wrong!';
                this.transferState = undefined;
                this.renderImageSrc = undefined;
            },
            () => {},
        );
    }

    loadRenderSettings() {
        this.minecraftBlenderRenderService.getRenderSettings(
            this.renderForm.get('renderFileSource')!.value,
        ).subscribe(
            (transfer) => {
                this.transferState = transfer;
                if (transfer.state == 'DONE') {
                    this.transferState = undefined;
                    this.loadedRenderSettings = transfer.event?.body;
                }
            },
            (error) => {
                this.errorMessage = 'Something went wrong!';
                this.transferState = undefined;
            },
            () => {},
        );
    }
}
