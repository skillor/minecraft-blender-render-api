import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
    selector: 'app-setup',
    templateUrl: './setup.component.html',
    styleUrls: ['./setup.component.scss']
})
export class SetupComponent implements OnInit {

    constructor(
        private router: Router,
        private route: ActivatedRoute,
    ) { }

    ngOnInit(): void {
        this.router.navigate(['home']);
    }

}
