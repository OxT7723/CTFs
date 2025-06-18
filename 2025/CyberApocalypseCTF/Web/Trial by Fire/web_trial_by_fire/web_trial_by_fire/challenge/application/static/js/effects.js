export class ParticleSystem {
    constructor() {
      this.container = document.createElement('div');
      this.container.className = 'particles-container';
      document.body.appendChild(this.container);
    }
  
    createEmber(x, y) {
      const ember = document.createElement('div');
      ember.className = 'ember';
      ember.style.left = `${x}px`;
      ember.style.top = `${y}px`;
      this.container.appendChild(ember);
  
      const angle = Math.random() * Math.PI * 2;
      const velocity = 2 + Math.random() * 2;
      const lifetime = 1000 + Math.random() * 2000;
      const startTime = Date.now();
  
      const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = elapsed / lifetime;
  
        if (progress >= 1) {
          ember.remove();
          return;
        }
  
        const currentX = parseFloat(ember.style.left) + Math.cos(angle) * velocity;
        const currentY = parseFloat(ember.style.top) - velocity;
        
        ember.style.left = `${currentX}px`;
        ember.style.top = `${currentY}px`;
        ember.style.opacity = Math.sin(progress * Math.PI);
  
        requestAnimationFrame(animate);
      };
  
      requestAnimationFrame(animate);
    }
  
    spawnEmbers(x, y, count = 10) {
      for (let i = 0; i < count; i++) {
        this.createEmber(x, y);
      }
    }
  }
  
  export function addVisualEffects(game) {
    const particles = new ParticleSystem();
  
    document.querySelectorAll('.button').forEach(button => {
      button.addEventListener('mouseover', () => {
        const rect = button.getBoundingClientRect();
        particles.spawnEmbers(rect.left + rect.width / 2, rect.top + rect.height / 2, 5);
      });
    });
  
    const originalHandlePlayerAction = game.handlePlayerAction.bind(game);
    game.handlePlayerAction = function(action) {
      const button = document.querySelector(`[data-action="${action}"]`);
      if (button) {
        const rect = button.getBoundingClientRect();
        
        switch(action) {
          case 'attack':
            button.style.animation = 'swordSlash 0.5s ease-out';
            particles.spawnEmbers(rect.left + rect.width / 2, rect.top, 15);
            break;
          case 'fireball':
            button.style.animation = 'fireballCast 0.5s ease-out';
            for (let i = 0; i < 20; i++) {
              setTimeout(() => {
                particles.spawnEmbers(rect.left + rect.width / 2, rect.top, 3);
              }, i * 50);
            }
            break;
          case 'lightning':
            button.style.animation = 'lightningStrike 0.5s ease-out';
            for (let i = 0; i < 3; i++) {
              setTimeout(() => {
                particles.spawnEmbers(rect.left + rect.width / 2, rect.top, 10);
              }, i * 200);
            }
            break;
        }
        
        setTimeout(() => {
          button.style.animation = '';
        }, 500);
      }
      
      originalHandlePlayerAction(action);
    };
  
    setInterval(() => {
      particles.spawnEmbers(
        Math.random() * window.innerWidth,
        window.innerHeight,
        1
      );
    }, 200);
  }