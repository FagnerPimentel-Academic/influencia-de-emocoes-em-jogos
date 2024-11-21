using UnityEngine;
using UnityEngine.SceneManagement;

public class DogController : MonoBehaviour
{
    private GameObject player; // Referência ao jogador
    public float followDistance = 2f; // Distância mínima para seguir
    public float followSpeed = 5f; // Velocidade de movimento
    public float jumpForce = 12f; // Força do pulo
    public int hp = 10;
    public bool isAlive = true;

    private Rigidbody2D rb2d;
    private AnimationController animationController;
    private SpriteRenderer spriteRenderer;
    private GameManager gameManager;
    private bool isGrounded;
    private bool hasObstacle;

    void Awake()
    {
        gameManager = GameManager.instance;
        player = GameObject.Find("Player");
        animationController = GetComponent<AnimationController>();
    }

    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        rb2d = GetComponent<Rigidbody2D>();
        Physics2D.IgnoreCollision(
            player.transform.GetComponent<Collider2D>(),
            GetComponent<Collider2D>()
        );
    }

    void Update()
    {
        if(isAlive && !hasObstacle)
            FollowPlayer();
    }

    void FollowPlayer()
    {
        float stopDistance = 0.06f;
        float distanceFromPlayer = Mathf.Abs(transform.position.x - player.transform.position.x);
        if (distanceFromPlayer + stopDistance > followDistance)
        {
            // Movimenta o cachorro em direção ao jogador
            Vector2 direction = (player.transform.position - transform.position).normalized;
            rb2d.velocity = new Vector2(direction.x * followSpeed, rb2d.velocity.y);

            animationController.PlayAnimation("dog_walk");

            // Inverte o sprite dependendo da direção
            if (direction.x > 0)
            {
                transform.localScale = new Vector3(1, 1, 1); // Olhando para a direita
            }
            else if (direction.x < 0)
            {
                transform.localScale = new Vector3(-1, 1, 1); // Olhando para a esquerda
            }

        }
        else
        {
            if (Mathf.Abs(rb2d.velocity.x) > 0.4f)
            {
                rb2d.velocity = new Vector2(rb2d.velocity.x / 1.08f, rb2d.velocity.y);
            }
            else
            {
                rb2d.velocity = new Vector2(0, rb2d.velocity.y);
                animationController.PlayAnimation("dog_idle");
            }
        }
            // Se o cachorro encontrar obstáculos (como diferença de altura), ele pula
            if (isGrounded && Mathf.Abs(rb2d.velocity.y) < 0.01f)
            {
                if (ShouldJump())
                {
                    Jump();
                }
            }
    }

    bool ShouldJump()
    {
        // Salta se o jogador estiver acima do cachorro
        return player.transform.position.y > transform.position.y + 0.5f && player.transform.position.y < transform.position.y + 3f;
    }

    void Jump()
    {
        rb2d.velocity = new Vector2(rb2d.velocity.x, 0); // Reseta a velocidade vertical
        rb2d.AddForce(new Vector2(0, jumpForce), ForceMode2D.Impulse); // Aplica força de pulo
    }

    // Verifica se o cachorro está no chão
    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.collider.CompareTag("Ground"))
        {
            isGrounded = true; // Está no chão
        }
    }

    // Quando sai do chão, não permite pulo
    private void OnCollisionExit2D(Collision2D collision)
    {
        if (collision.collider.CompareTag("Ground"))
        {
            isGrounded = false; // Saiu do chão
        }
    }

    void OnTriggerEnter2D(Collider2D col)
    {
        hasObstacle = col.tag == "Ground";
        hasObstacle = col.name == "Werewolf";
    }

    void OnTriggerExit2D(Collider2D col)
    {
        if (col.tag == "Ground")
            hasObstacle = false;

        if (col.name == "Werewolf")
            hasObstacle = false;
    }


    public void Hurt(int damage)
    {
        hp -= damage;

        spriteRenderer.color = Color.red;
        Invoke("ResetColor", 0.1f);

        if (hp < 1)
        {
            isAlive = false;
            animationController.PlayAnimation("dog_death");
            Invoke("ResetGame", 10);
        }
    }

    private void ResetColor()
    {
        spriteRenderer.color = Color.white;
    }

    private void ResetGame()
    {
        gameManager.GetComponent<EmotionManager>().CloseServer();
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

}
