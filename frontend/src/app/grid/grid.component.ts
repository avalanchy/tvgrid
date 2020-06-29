import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Title } from '../interfaces';

@Component({
  selector: 'app-grid',
  templateUrl: './grid.component.html',
  styleUrls: ['./grid.component.css']
})
export class GridComponent implements OnInit {

  title: Title;

  constructor(private http: HttpClient) { }

  async ngOnInit() {
    this.title = await this.http.get<Title>("/api/titles/tt0096697/").toPromise();
    console.log(this.title);
  }

}
