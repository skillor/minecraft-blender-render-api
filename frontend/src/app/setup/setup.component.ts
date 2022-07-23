import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MinecraftBlenderRenderService } from '../shared/minecraft-blender-render/minecraft-blender-render.service';

@Component({
    selector: 'app-setup',
    templateUrl: './setup.component.html',
    styleUrls: ['./setup.component.scss']
})
export class SetupComponent implements OnInit {

    error: string = '';

    constructor(
        private router: Router,
        private minecraftBlenderRenderService: MinecraftBlenderRenderService,
    ) { }

    ngOnInit(): void {
        this.minecraftBlenderRenderService.checkEndpoint().subscribe(
            (success) => {
                this.router.navigate(['home']);
            },
            (error) => {
                this.error = 'Api Endpoint is not valid!';
            },
            () => {},
        );
    }

}
