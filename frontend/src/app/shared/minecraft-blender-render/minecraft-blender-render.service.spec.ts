import { TestBed } from '@angular/core/testing';

import { MinecraftBlenderRenderService } from './minecraft-blender-render.service';

describe('MinecraftBlenderRenderService', () => {
  let service: MinecraftBlenderRenderService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MinecraftBlenderRenderService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
