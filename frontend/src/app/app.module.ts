import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SettingsComponent } from './pages/settings/settings.component';
import { SetupComponent } from './setup/setup.component';

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        SettingsComponent,
        SetupComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
