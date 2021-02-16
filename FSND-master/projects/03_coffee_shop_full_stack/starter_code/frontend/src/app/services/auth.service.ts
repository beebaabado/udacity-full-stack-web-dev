import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { environment } from '../../environments/environment';

const JWTS_LOCAL_KEY = 'JWTS_LOCAL_KEY';
const JWTS_ACTIVE_INDEX_KEY = 'JWTS_ACTIVE_INDEX_KEY';

export interface UserProfile {
  sub: string;
  nickname: string;
  name: string;
  picture: string;
  updated_at: string;
  email: string;
  email_verified: string;
} 

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  url = environment.auth0.url;
  audience = environment.auth0.audience;
  clientId = environment.auth0.clientId;
  callbackURL = environment.auth0.callbackURL;
 
  token: string;
  header: any;
  payload: any;
  user_name: string;
  public user_info: UserProfile;
  public tokenexptime: Date;

  constructor(private http: HttpClient,
              private jwtservice: JwtHelperService) { }

  build_login_link(callbackPath = '') {
    let link = 'https://';
    link += this.url + '.auth0.com';
    link += '/authorize?';
    link += 'audience=' + this.audience + '&';
    link += 'response_type=token&';
    link += 'client_id=' + this.clientId + '&';
    link += 'scope=' + 'openid%20profile%20email&';
    link += 'redirect_uri=' + this.callbackURL + callbackPath;
    return link;
  }
  
  // invoked in app.component on load
  check_token_fragment() {
    // parse the fragment
    const fragment = window.location.hash.substr(1).split('&')[0].split('=');
    // check if the fragment includes the access token
    if ( fragment[0] === 'access_token' ) {
      // add the access token to the jwt
      this.token = fragment[1];
      // save jwts to localstore
      this.set_jwt();
    }
  }

  set_jwt() {
    localStorage.setItem(JWTS_LOCAL_KEY, this.token);
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  load_jwts() {
    this.token = localStorage.getItem(JWTS_LOCAL_KEY) || null;
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  activeJWT() {
    return this.token;
  }

  decodeJWT(token: string) {
    //const jwtservice = new JwtHelperService();
    this.payload = this.jwtservice.decodeToken(token);
    return this.payload;
  }

  logout() {
    this.token = '';
    this.payload = null;
    this.set_jwt();
  }
  
  sessionLogout(callbackPath = ''){
    console.log("User session logout.")
    // Following results in CORS error...revist later
    const  authLogoutEndptUri = 'https://' + this.url + '.auth0.com/v2/logout?client_id=' + this.clientId + '&' + 'returnTo=' + this.callbackURL + callbackPath;
    console.log (authLogoutEndptUri);
    
    //header with 
    const header = {
      headers: new HttpHeaders()
        .set('Access-Control-Allow-Origin',  '*')
    };

    this.http.get(authLogoutEndptUri, header)
      .subscribe( 
        () => {console.log("logout"); this.logout();},
        (err) => console.error(err)
      );
    }

  isExpired() {
    if (this.jwtservice.isTokenExpired(this.activeJWT())) {
      // token expired
      this.logout();
      return true;
    } else {
      // token valid
      return false;
    }
  }
  
  getExpiredTime() {
    if (this.payload) { 
      if (this.payload['exp']) {
        this.tokenexptime = new Date(this.payload['exp'] * 1000); 
      }
    }
  }

  can(permission: string) {
    return this.payload && this.payload.permissions && this.payload.permissions.length && this.payload.permissions.indexOf(permission) >= 0;
  }
  
  getAuthorizationHeader() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Bearer ${this.activeJWT()}`)
    };
    return header;
  }

  getUserName(){
    // use login bearer token which is attached to angular http request header to get user info via Auth0 /userinfo endpoint
    const userinfoUrl = 'https://' + this.url + '.auth0.com/userinfo';
    this.http.get(userinfoUrl, this.getAuthorizationHeader())
      .subscribe((data: UserProfile) => this.user_info = { ...data },
         (err) => console.error(err)
      );
 }
}