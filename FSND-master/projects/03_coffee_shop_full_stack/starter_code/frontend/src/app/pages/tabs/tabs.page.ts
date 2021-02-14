import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  styleUrls: ['tabs.page.scss']
})

export class TabsPage implements OnInit {
  Object = Object;
  
  constructor(
    public auth: AuthService,
    ) { 
      }
     
    ngOnInit() {
      try {
        this.auth.getUserName();
      }
      catch(err){
        console.log(err);
      } 
    }
}

