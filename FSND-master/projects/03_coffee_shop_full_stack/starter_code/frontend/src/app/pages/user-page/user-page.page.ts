import { Component, OnInit } from '@angular/core';
import { IonDatetime } from '@ionic/angular';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.page.html',
  styleUrls: ['./user-page.page.scss'],
})
export class UserPagePage implements OnInit {
  loginURL: string;
  firstLogin: boolean = false;

  constructor(public auth: AuthService) {
   this.user_login();
  }
  ngOnInit() {
    console.log("userpage:ngInit");
    if (this.auth.isExpired()){
       this.firstLogin= true;
    }
  }

  ionViewWillEnter() {
    console.log("userpage:ionViewWillEnter");
    // logs out user if token is expired and prompts user for relogin
    if (this.firstLogin){
      this.user_login();
      this.firstLogin = false;
    }
    else if (this.auth.isExpired()) {
        this.user_login();
      }
  }

  user_login() {
    this.loginURL = this.auth.build_login_link('/tabs/user-page');
    this.auth.getExpiredTime();
  }
}


